from datetime import datetime, timedelta, timezone as datetime_timezone
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.db import connection
from django.template.loader import get_template
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from predictor.apps.fixtures.models import Fixture, Team
from predictor.apps.picks.models import Pick
from predictor.apps.results.models import UserScores, UserTotalResult, UserWeekResult
from scripts.get_week import get_week

User = get_user_model()
UTC = datetime_timezone.utc


class PredictorTestCase(TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 24, 18, tzinfo=UTC)
        clock = patch('django.utils.timezone.now', return_value=self.now)
        clock.start()
        self.addCleanup(clock.stop)
        season = override_settings(SEASON_WEEK_ONE_END=(self.now + timedelta(days=1)).isoformat())
        season.enable()
        self.addCleanup(season.disable)
        self.user = User.objects.create_user('player', password='test-password')
        self.other = User.objects.create_user('opponent', password='test-password')
        self.away = Team.objects.create(short_name='BUF', team_name='Bills')
        self.home = Team.objects.create(short_name='NYJ', team_name='Jets')
        self.fixture = self.make_fixture()
        self.pick = Pick.objects.create(user=self.user, fixture=self.fixture,
                                        away_pick=20, home_pick=30)
        self.other_pick = Pick.objects.create(user=self.other, fixture=self.fixture,
                                              away_pick=17, home_pick=24)
        self.client.force_login(self.user)

    def make_fixture(self, hours=2, week=1, changeable=True):
        return Fixture.objects.create(
            name='Bills at Jets', away_team=self.away, home_team=self.home,
            away_score=0, home_score=0, week=week, changeable=changeable,
            ko_datetime=self.now + timedelta(hours=hours),
        )

    def pick_payload(self, pick=None, **changes):
        data = {
            'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '1',
            'form-MIN_NUM_FORMS': '0', 'form-MAX_NUM_FORMS': '1000',
            'form-0-id': str((pick or self.pick).pk),
            'form-0-away_pick': '21', 'form-0-home_pick': '28', 'action': 'save',
        }
        data.update(changes)
        return data


class PickSecurityTests(PredictorTestCase):
    def test_anonymous_users_cannot_read_or_edit_picks(self):
        self.client.logout()
        for name in ['all', 'public', 'check', 'simple', 'update']:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse('picks:' + name)).status_code, 302)

    def test_own_pick_saves_and_redirects(self):
        response = self.client.post(reverse('picks:update'), self.pick_payload())
        self.assertRedirects(response, reverse('picks:all'))
        self.pick.refresh_from_db()
        self.assertEqual((self.pick.away_pick, self.pick.home_pick), (21, 28))

    def test_other_users_pick_cannot_be_updated(self):
        response = self.client.post(reverse('picks:update'), self.pick_payload(self.other_pick))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['formset'].errors)
        self.other_pick.refresh_from_db()
        self.assertEqual(self.other_pick.away_pick, 17)

    def test_fixture_and_user_fields_cannot_be_reassigned(self):
        target = self.make_fixture(hours=-4)
        response = self.client.post(reverse('picks:update'), self.pick_payload(**{
            'form-0-fixture': str(target.pk), 'form-0-user': str(self.other.pk),
        }))
        self.assertEqual(response.status_code, 302)
        self.pick.refresh_from_db()
        self.assertEqual(self.pick.fixture_id, self.fixture.pk)
        self.assertEqual(self.pick.user_id, self.user.pk)

    def test_pick_locks_at_exactly_one_hour_before_kickoff(self):
        self.fixture.ko_datetime = self.now + timedelta(hours=1)
        self.fixture.save()
        response = self.client.get(reverse('picks:update'))
        self.assertEqual(len(response.context['formset'].forms), 0)
        response = self.client.post(reverse('picks:update'), self.pick_payload())
        self.assertEqual(response.status_code, 200)
        self.pick.refresh_from_db()
        self.assertEqual(self.pick.away_pick, 20)

    def test_form_opened_before_deadline_cannot_save_afterwards(self):
        self.assertEqual(len(self.client.get(reverse('picks:update')).context['formset'].forms), 1)
        with patch('django.utils.timezone.now', return_value=self.now + timedelta(hours=1)):
            response = self.client.post(reverse('picks:update'), self.pick_payload())
        self.assertEqual(response.status_code, 200)
        self.pick.refresh_from_db()
        self.assertEqual(self.pick.away_pick, 20)

    def test_played_game_cannot_be_edited(self):
        self.fixture.ko_datetime = self.now - timedelta(hours=2)
        self.fixture.save()
        self.client.post(reverse('picks:update'), self.pick_payload())
        self.pick.refresh_from_db()
        self.assertEqual(self.pick.away_pick, 20)

    def test_deadline_is_rechecked_after_loading_the_database_rows(self):
        from predictor.apps.picks.forms import PickForm

        form = PickForm({'away_pick': '21', 'home_pick': '28'}, instance=self.pick)
        with patch('django.utils.timezone.now', return_value=self.now + timedelta(hours=1)):
            self.assertFalse(form.is_valid())
        self.assertIn('This pick has closed', str(form.non_field_errors()))

    def test_other_weeks_and_archived_fixtures_cannot_be_edited(self):
        for fixture in [self.make_fixture(week=2), self.make_fixture(changeable=False)]:
            pick = Pick.objects.create(user=self.user, fixture=fixture, away_pick=10, home_pick=14)
            response = self.client.post(reverse('picks:update'), self.pick_payload(pick))
            self.assertEqual(response.status_code, 200)
            pick.refresh_from_db()
            self.assertEqual(pick.away_pick, 10)

    def test_forged_initial_form_count_cannot_create_a_new_pick(self):
        before = Pick.objects.count()
        response = self.client.post(reverse('picks:update'), self.pick_payload(**{
            'form-INITIAL_FORMS': '0',
        }))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['formset'].non_form_errors())
        self.assertEqual(Pick.objects.count(), before)

    def test_duplicate_ids_reject_the_whole_submission(self):
        response = self.client.post(reverse('picks:update'), self.pick_payload(**{
            'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2',
            'form-1-id': str(self.pick.pk),
            'form-1-away_pick': '1', 'form-1-home_pick': '2',
        }))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['formset'].non_form_errors())
        self.pick.refresh_from_db()
        self.assertEqual(self.pick.away_pick, 20)

    def test_one_invalid_row_prevents_partial_saves(self):
        response = self.client.post(reverse('picks:update'), self.pick_payload(**{
            'form-TOTAL_FORMS': '2', 'form-INITIAL_FORMS': '2',
            'form-1-id': str(self.other_pick.pk),
            'form-1-away_pick': '1', 'form-1-home_pick': '2',
        }))
        self.assertEqual(response.status_code, 200)
        self.pick.refresh_from_db()
        self.assertEqual(self.pick.away_pick, 20)

    def test_missing_management_form_is_shown(self):
        response = self.client.post(reverse('picks:update'), {'action': 'save'})
        self.assertContains(response, 'ManagementForm')

    def test_negative_and_partial_scores_show_errors(self):
        for value in ['-1', '']:
            response = self.client.post(reverse('picks:update'), self.pick_payload(**{
                'form-0-away_pick': value,
            }))
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context['formset'].is_valid())
            self.pick.refresh_from_db()
            self.assertEqual(self.pick.away_pick, 20)

    def test_all_public_routes_hide_unlocked_predictions(self):
        closed = self.make_fixture(hours=1)
        closed_pick = Pick.objects.create(user=self.other, fixture=closed, away_pick=7, home_pick=10)
        for route in ['public', 'check', 'simple']:
            for week in ['', '?week=1', '?week=All']:
                with self.subTest(route=route, week=week):
                    response = self.client.get(reverse('picks:' + route) + week)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(list(response.context['object_list']), [closed_pick])

    def test_own_picks_remain_visible_after_deadline(self):
        self.fixture.ko_datetime = self.now - timedelta(days=1)
        self.fixture.save()
        response = self.client.get(reverse('picks:all') + '?week=All')
        self.assertEqual(list(response.context['object_list']), [self.pick])

    def test_public_rows_are_grouped_by_fixture_even_for_matching_kickoff_times(self):
        self.fixture.ko_datetime = self.now
        self.fixture.save()
        second_fixture = self.make_fixture(hours=0)
        second_picks = [Pick.objects.create(user=user, fixture=second_fixture)
                        for user in [self.user, self.other]]
        response = self.client.get(reverse('picks:public'))
        self.assertEqual(list(response.context['object_list']),
                         [self.pick, self.other_pick] + second_picks)


class FixturePermissionTests(PredictorTestCase):
    def payload(self, **changes):
        data = {
            'form-TOTAL_FORMS': '1', 'form-INITIAL_FORMS': '1',
            'form-0-id': str(self.fixture.pk),
            'form-0-away_score': '17', 'form-0-home_score': '24', 'action': 'save',
        }
        data.update(changes)
        return data

    def grant_edit(self):
        self.user.user_permissions.add(Permission.objects.get(
            content_type__app_label='fixtures', codename='change_fixture'))

    def test_regular_user_cannot_read_or_post_score_editor(self):
        self.assertEqual(self.client.get(reverse('fixtures:update')).status_code, 403)
        self.assertEqual(self.client.post(reverse('fixtures:update'), self.payload()).status_code, 403)
        self.fixture.refresh_from_db()
        self.assertEqual(self.fixture.home_score, 0)

    def test_staff_without_permission_cannot_edit_scores(self):
        self.user.is_staff = True
        self.user.save()
        self.assertEqual(self.client.post(reverse('fixtures:update'), self.payload()).status_code, 403)

    def test_authorized_score_update_redirects(self):
        self.grant_edit()
        response = self.client.post(reverse('fixtures:update'), self.payload())
        self.assertRedirects(response, reverse('fixtures:all'))
        self.fixture.refresh_from_db()
        self.assertEqual(self.fixture.home_score, 24)

    def test_authorized_user_cannot_forge_an_out_of_scope_fixture(self):
        self.grant_edit()
        fixture = self.make_fixture(week=2)
        response = self.client.post(reverse('fixtures:update'), self.payload(**{
            'form-0-id': str(fixture.pk),
        }))
        self.assertEqual(response.status_code, 200)
        fixture.refresh_from_db()
        self.assertEqual(fixture.home_score, 0)

    def test_blank_scores_are_validation_errors_not_database_errors(self):
        self.grant_edit()
        response = self.client.post(reverse('fixtures:update'), self.payload(**{
            'form-0-away_score': '',
        }))
        self.assertContains(response, 'Enter a score')
        self.fixture.refresh_from_db()
        self.assertEqual(self.fixture.home_score, 0)


class AccountAndPageTests(PredictorTestCase):
    def test_invalid_week_queries_return_404(self):
        for route in ['fixtures:all', 'picks:all', 'picks:public', 'picks:check',
                      'picks:simple', 'results:all']:
            for value in ['banana', '0', '24', '-1']:
                with self.subTest(route=route, value=value):
                    response = self.client.get(reverse(route), {'week': value})
                    self.assertEqual(response.status_code, 404)

    def test_logout_requires_post_and_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.get(reverse('accounts:logout')).status_code, 405)
        self.assertEqual(client.post(reverse('accounts:logout')).status_code, 403)
        response = client.get(reverse('picks:all'))
        self.assertContains(response, 'method="post"')
        response = client.post(reverse('accounts:logout'), {
            'csrfmiddlewaretoken': client.cookies['csrftoken'].value,
        })
        self.assertRedirects(response, reverse('thanks'))
        self.assertNotIn('_auth_user_id', client.session)

    def test_login_with_upgraded_framework(self):
        self.client.logout()
        response = self.client.post(reverse('accounts:login'), {
            'username': 'player', 'password': 'test-password',
        })
        self.assertRedirects(response, reverse('test'))

    def test_missing_kickoff_does_not_crash_my_picks(self):
        self.fixture.ko_datetime = None
        self.fixture.save()
        self.assertEqual(self.client.get(reverse('picks:all')).status_code, 200)
        self.assertEqual(self.pick.points_scored, 0)

    def test_future_fixture_with_scores_does_not_award_points(self):
        self.fixture.home_score = self.pick.home_pick
        self.fixture.away_score = self.pick.away_pick
        self.assertEqual(self.pick.points_scored, 0)

    def test_all_templates_compile(self):
        root = Path(__file__).resolve().parent.parent
        for directory in [root / 'templates', *root.glob('predictor/apps/*/templates')]:
            for path in directory.rglob('*.html'):
                with self.subTest(template=str(path)):
                    get_template(str(path.relative_to(directory)))


class WeekCalculationTests(SimpleTestCase):
    rollover = datetime(2026, 9, 16, 5, tzinfo=UTC)

    def test_rollover_boundary_and_clamping(self):
        for delta, expected in [(-1, 1), (0, 2), (7, 3), (140, 22), (365, 22)]:
            with self.subTest(delta=delta):
                date = self.rollover + timedelta(days=delta)
                self.assertEqual(get_week(date, self.rollover), expected)

    @override_settings(SEASON_WEEK_ONE_END='2026-09-16T05:00:00+00:00')
    def test_default_now_is_evaluated_on_every_call(self):
        for delta, expected in [(-1, 1), (7, 3)]:
            with patch('django.utils.timezone.now', return_value=self.rollover + timedelta(days=delta)):
                self.assertEqual(get_week(), expected)

    def test_naive_legacy_arguments_are_interpreted_as_utc(self):
        self.assertEqual(get_week(datetime(2026, 9, 23, 5), datetime(2026, 9, 16, 5)), 3)

    @override_settings(SEASON_WEEK_ONE_END='invalid')
    def test_bad_season_configuration_has_a_clear_error(self):
        with self.assertRaisesMessage(ImproperlyConfigured, 'ISO 8601'):
            get_week()


@override_settings(SEASON_WEEK_ONE_END='')
class ScheduleWeekTests(TestCase):
    def test_no_active_schedule_defaults_to_week_one(self):
        self.assertEqual(get_week(), 1)

    def test_active_schedule_replaces_the_hardcoded_2024_season(self):
        for year, active in [(2024, False), (2026, True)]:
            Fixture.objects.create(name='Opening game', week=1, changeable=active,
                                   ko_datetime=datetime(year, 9, 10, 0, tzinfo=UTC),
                                   away_score=0, home_score=0)
        self.assertEqual(get_week(datetime(2026, 9, 16, 4, 59, tzinfo=UTC)), 1)
        self.assertEqual(get_week(datetime(2026, 9, 16, 5, tzinfo=UTC)), 2)


class LeaderboardIntegrationTests(PredictorTestCase):
    @classmethod
    def setUpClass(cls):
        # View DDL must run before TestCase opens its transaction on MySQL.
        call_command('install_score_views', verbosity=0)
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.fixture.ko_datetime = self.now - timedelta(hours=5)
        self.fixture.away_score, self.fixture.home_score = 20, 30
        self.fixture.save()
        for user in [self.user, self.other]:
            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO results_userweekresult (week, user_id) VALUES (%s, %s)',
                               [1, user.pk])
            UserTotalResult.objects.create(id=user.pk, user=user)

    def test_score_views_match_the_documented_points_and_have_unique_ids(self):
        rows = list(UserScores.objects.order_by('user_id'))
        self.assertEqual([row.pk for row in rows], [self.pick.pk, self.other_pick.pk])
        self.assertEqual([row.fixture_id for row in rows], [self.fixture.pk] * 2)
        self.assertEqual([row.user_points for row in rows], [45, 33])
        self.assertEqual(len(set(UserWeekResult.objects.values_list('pk', flat=True))), 2)
        self.assertEqual(UserTotalResult.objects.get(user=self.user).total_points_scored, 45)

    def test_results_page_renders_against_real_database_views(self):
        response = self.client.get(reverse('results:all') + '?week=All')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['valid_picks']), 2)

    def test_blank_predictions_preserve_the_existing_30_20_default(self):
        self.pick.away_pick = self.pick.home_pick = None
        self.pick.save()
        row = UserScores.objects.get(pk=self.pick.pk)
        self.assertEqual((int(row.away_pick), int(row.home_pick), row.user_points), (20, 30, 45))
