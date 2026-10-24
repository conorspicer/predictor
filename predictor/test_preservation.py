"""Behavior checks for the preserved game, beyond the security regression tests."""
from datetime import datetime, timedelta, timezone as datetime_timezone
from io import BytesIO, StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command, CommandError
from django.db import connection
from django.forms import modelform_factory
from django.test import Client, TestCase, TransactionTestCase, override_settings
from django.urls import reverse

from predictor.apps.fixtures.models import Fixture, Team
from predictor.apps.picks.models import Pick
from predictor.apps.playoff_teams.models import PlayoffPick
from predictor.apps.results.models import UserScores
from predictor.tests import PredictorTestCase

User = get_user_model()


class SignUpCompatibilityTests(TestCase):
    def test_signup_form_and_password_validation_work_with_bootstrap_helper(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertContains(response, 'Display name')
        self.assertContains(response, 'Email address')
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'new-player', 'email': 'new-player@example.test',
            'password1': 'Preservation-example-2026!',
            'password2': 'Preservation-example-2026!',
        })
        self.assertRedirects(response, reverse('login'))
        player = User.objects.get(username='new-player')
        self.assertTrue(player.check_password('Preservation-example-2026!'))
        self.assertTrue(self.client.login(username='new-player', password='Preservation-example-2026!'))

    def test_signup_rejects_invalid_passwords_and_duplicate_names(self):
        User.objects.create_user('existing-player')
        response = self.client.post(reverse('accounts:signup'), {
            'username': 'existing-player', 'email': 'new@example.test',
            'password1': '123', 'password2': 'different',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
        self.assertEqual(User.objects.count(), 1)

    @override_settings(PASSWORD_HASHERS=['django.contrib.auth.hashers.PBKDF2PasswordHasher'])
    def test_older_pbkdf2_passwords_still_verify_and_are_upgraded_on_login(self):
        player = User.objects.create(username='older-hash')
        player.password = PBKDF2PasswordHasher().encode(
            'Preservation-example-2026!', 'synthetic-legacy-salt', iterations=390000,
        )
        old_hash = player.password
        player.save()
        response = self.client.post(reverse('accounts:login'), {
            'username': player.username, 'password': 'Preservation-example-2026!',
        })
        self.assertRedirects(response, reverse('test'))
        player.refresh_from_db()
        self.assertNotEqual(player.password, old_hash)
        self.assertTrue(player.check_password('Preservation-example-2026!'))


class PlayoffCompatibilityTests(PredictorTestCase):
    def setUp(self):
        super().setUp()
        self.away.division, self.away.conference = 'AFC_EAST', 'AFC'
        self.away.save()
        self.nfc = Team.objects.create(short_name='DAL', team_name='Cowboys',
                                       division='NFC_EAST', conference='NFC')
        self.playoffs = PlayoffPick.objects.create(user=self.user)
        self.opponent = PlayoffPick.objects.create(user=self.other, afc_east=self.away)

    def test_playoff_picks_save_and_remain_owned_by_the_logged_in_player(self):
        self.assertEqual(self.client.get(reverse('playoff_teams:update')).status_code, 200)
        response = self.client.post(reverse('playoff_teams:update'), {
            'afc_east': self.away.pk, 'nfc_east': self.nfc.pk,
            'sb_runner_up': self.away.pk, 'sb_winner': self.nfc.pk,
            'user': self.other.pk, 'id': self.opponent.pk,
        })
        self.assertRedirects(response, reverse('playoff_teams:all'))
        self.playoffs.refresh_from_db()
        self.opponent.refresh_from_db()
        self.assertEqual(self.playoffs.sb_winner, self.nfc)
        self.assertEqual(self.playoffs.user, self.user)
        self.assertIsNone(self.opponent.sb_winner)

    def test_wrong_division_and_conference_are_rejected_with_visible_errors(self):
        response = self.client.post(reverse('playoff_teams:update'), {
            'afc_east': self.nfc.pk, 'afc_wild1': self.nfc.pk,
        })
        self.assertContains(response, 'Select a valid choice')
        self.playoffs.refresh_from_db()
        self.assertIsNone(self.playoffs.afc_east)
        self.assertIsNone(self.playoffs.afc_wild1)

    def test_private_playoff_list_does_not_include_an_opponents_entry(self):
        response = self.client.get(reverse('playoff_teams:all'))
        self.assertEqual(list(response.context['object_list']), [self.playoffs])
        self.assertContains(response, '/static/images/NFL-logo.png')
        self.assertNotContains(response, 'src="/static/"')

    def test_anonymous_players_cannot_read_or_edit_playoff_entries(self):
        self.client.logout()
        for route in ['all', 'update', 'public']:
            self.assertEqual(self.client.get(reverse('playoff_teams:' + route)).status_code, 302)

    def test_unprovisioned_player_gets_404_instead_of_server_error(self):
        self.playoffs.delete()
        self.assertEqual(self.client.get(reverse('playoff_teams:update')).status_code, 404)


class ImageUploadCompatibilityTests(TestCase):
    def test_real_pillow_image_validation_and_storage(self):
        form_class = modelform_factory(Team, fields=['team_name', 'team_logo'])
        png = BytesIO()
        Image.new('RGB', (4, 4), color='blue').save(png, format='PNG')
        with TemporaryDirectory() as directory, override_settings(MEDIA_ROOT=directory):
            form = form_class({'team_name': 'Bills'}, {
                'team_logo': SimpleUploadedFile('test-logo.png', png.getvalue(), 'image/png'),
            })
            self.assertTrue(form.is_valid(), form.errors)
            team = form.save()
            with Image.open(team.team_logo.path) as image:
                self.assertEqual((image.format, image.size), ('PNG', (4, 4)))

    def test_corrupt_image_is_rejected(self):
        form_class = modelform_factory(Team, fields=['team_name', 'team_logo'])
        form = form_class({'team_name': 'Bills'}, {
            'team_logo': SimpleUploadedFile('bad.png', b'not an image', 'image/png'),
        })
        self.assertFalse(form.is_valid())
        self.assertIn('team_logo', form.errors)


class ScoringPreservationTests(PredictorTestCase):
    @classmethod
    def setUpClass(cls):
        call_command('install_score_views', stdout=StringIO())
        super().setUpClass()

    def test_historical_scoring_cases_match_in_python_and_database(self):
        # Actual away/home, predicted away/home, expected winner/margin/total points.
        examples = [
            ((20, 30), (20, 30), (25, 10, 10)),
            ((20, 30), (17, 24), (25, 7, 1)),
            ((20, 30), (30, 20), (0, 10, 10)),
            ((27, 20), (24, 21), (25, 6, 8)),
            ((14, 14), (14, 14), (25, 10, 10)),
            ((0, 7), (0, 7), (25, 10, 10)),
            ((10, 40), (0, 100), (25, 0, 0)),
            ((20, 30), (20, 20), (0, 0, 0)),
        ]
        for actual, predicted, expected in examples:
            for locked in [False, True]:
                with self.subTest(actual=actual, predicted=predicted, locked=locked):
                    fixture = self.make_fixture(hours=-6)
                    fixture.away_score, fixture.home_score = actual
                    fixture.save()
                    pick = Pick.objects.create(user=self.user, fixture=fixture,
                                                away_pick=predicted[0], home_pick=predicted[1],
                                                lock=locked)
                    self.assertEqual((pick.winner_pts, pick.margin_pts, pick.totalpts_pts), expected)
                    sql = UserScores.objects.get(pk=pick.pk)
                    self.assertEqual((sql.winner_pts, sql.margin_pts, sql.total_score_pts), expected)
                    self.assertEqual(sql.user_points, sum(expected))

    def test_future_games_do_not_award_database_points(self):
        # The SQL views use the database clock, not the patched Django clock.
        self.fixture.ko_datetime = datetime.now(datetime_timezone.utc) + timedelta(days=2)
        self.fixture.away_score, self.fixture.home_score = 20, 30
        self.fixture.save()
        self.assertEqual(UserScores.objects.get(pk=self.pick.pk).user_points, 0)

class DemoCommandTests(TransactionTestCase):
    def tearDown(self):
        # This historic backing table has no current managed model for flush().
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM results_userweekresult')
        super().tearDown()

    @override_settings(DEBUG=True, SEASON_WEEK_ONE_END='')
    def test_fresh_demo_provisions_the_whole_four_player_game(self):
        call_command('seed_demo', stdout=StringIO())
        self.assertEqual((User.objects.count(), Team.objects.count(), Fixture.objects.count(),
                          Pick.objects.count(), PlayoffPick.objects.count()), (4, 8, 5, 20, 4))
        root = Path(settings.BASE_DIR) / 'static'
        for team in Team.objects.all():
            self.assertTrue((root / team.team_logo.name).is_file(), team.team_logo.name)
        client = Client()
        self.assertTrue(client.login(username='conorspicer', password='demo-only-predictor'))
        for route in ['home', 'test', 'thanks', 'HOF', 'fixtures:all', 'fixtures:update',
                      'picks:all', 'picks:update', 'picks:public', 'picks:check', 'picks:simple',
                      'playoff_teams:all', 'playoff_teams:update', 'playoff_teams:public',
                      'results:all', 'admin:index', 'admin:fixtures_team_changelist',
                      'admin:fixtures_fixture_changelist', 'admin:picks_pick_changelist',
                      'admin:playoff_teams_playoffpick_changelist',
                      'admin:results_usertotalresult_changelist',
                      'admin:results_userweekresult_changelist']:
            with self.subTest(route=route):
                self.assertEqual(client.get(reverse(route)).status_code, 200)

        # DDL belongs outside TestCase's atomic wrapper on MySQL.
        before = list(Pick.objects.order_by('pk').values_list('pk', 'away_pick', 'home_pick'))
        call_command('install_score_views', stdout=StringIO())
        self.assertEqual(list(Pick.objects.order_by('pk').values_list('pk', 'away_pick', 'home_pick')), before)

    @override_settings(DEBUG=True)
    def test_demo_refuses_to_overwrite_existing_data(self):
        player = User.objects.create_user('keep-me')
        with self.assertRaisesMessage(CommandError, 'Existing data was left unchanged'):
            call_command('seed_demo', stdout=StringIO())
        self.assertTrue(User.objects.filter(pk=player.pk).exists())

    @override_settings(DEBUG=False)
    def test_demo_requires_explicit_development_mode(self):
        with self.assertRaisesMessage(CommandError, 'DJANGO_DEBUG=true'):
            call_command('seed_demo', stdout=StringIO())
        self.assertFalse(User.objects.exists())
