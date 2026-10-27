from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.utils import timezone

from predictor.apps.fixtures.models import Fixture, Team
from predictor.apps.picks.models import Pick
from predictor.apps.playoff_teams.models import PlayoffPick
from predictor.apps.results.models import UserTotalResult
from scripts.get_week import get_week


class Command(BaseCommand):
    help = 'Populate an empty development database with fictional Predictor examples.'

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError('Demo data requires DJANGO_DEBUG=true.')
        User = get_user_model()
        if User.objects.exists() or Team.objects.exists() or Fixture.objects.exists():
            raise CommandError('Use an empty demo database. Existing data was left unchanged.')
        now = timezone.now()
        with transaction.atomic():
            players = []
            for index, name in enumerate([
                'conorspicer', 'torinmehmet', 'magnusmartinsen', 'lewismead',
            ]):
                player = User.objects.create_user(
                    name, email=f'{name}@example.test', password='demo-only-predictor',
                    is_staff=index == 0, is_superuser=index == 0,
                )
                players.append(player)
                UserTotalResult.objects.create(id=player.pk, user=player)
                # The historic app used this table as its season/week roster.
                with connection.cursor() as cursor:
                    cursor.executemany(
                        'INSERT INTO results_userweekresult (week, user_id) VALUES (%s, %s)',
                        [(week, player.pk) for week in range(1, 24)],
                    )
            teams = {}
            examples = [
                ('BUF', 'Bills', 'AFC_EAST', 'AFC', 'buffalo-bills-logo-vector-01.png'),
                ('BAL', 'Ravens', 'AFC_NORTH', 'AFC', 'baltimore-ravens-logo-vector-01.png'),
                ('HOU', 'Texans', 'AFC_SOUTH', 'AFC', 'houston-texans-logo-vector.png'),
                ('KC', 'Chiefs', 'AFC_WEST', 'AFC', 'kansas-city-chiefs-vector-logo.png'),
                ('DAL', 'Cowboys', 'NFC_EAST', 'NFC', 'dallas-cowboys-logo-vector.png'),
                ('GB', 'Packers', 'NFC_NORTH', 'NFC', 'green-bay-packers-logo-vector.png'),
                ('ATL', 'Falcons', 'NFC_SOUTH', 'NFC', 'atlanta-falcons-logo-vector.png'),
                ('SF', '49ers', 'NFC_WEST', 'NFC', '49ers_Logo.png'),
            ]
            for short, name, division, conference, logo in examples:
                teams[short] = Team.objects.create(
                    short_name=short, team_name=name, full_name=name,
                    division=division, conference=conference, team_logo=f'logos/{logo}',
                )
            # Scores and timings are fictional, never an imported NFL schedule.
            finished = Fixture.objects.create(
                name='Demo completed game', away_team=teams['BUF'], home_team=teams['DAL'],
                away_score=20, home_score=30, week=1, ko_datetime=now - timedelta(hours=6),
            )
            week = get_week()
            fixtures = [finished]
            for name, away, home, hours, fixture_week in [
                ('Demo closed picks', 'BAL', 'GB', 0.5, week),
                ('Demo editable picks', 'HOU', 'ATL', 3, week),
                ('Demo second editable game', 'KC', 'SF', 4, week),
                ('Demo following week', 'BUF', 'GB', 24 * 7, min(week + 1, 22)),
            ]:
                fixtures.append(Fixture.objects.create(
                    name=name, away_team=teams[away], home_team=teams[home],
                    away_score=0, home_score=0, week=fixture_week,
                    ko_datetime=now + timedelta(hours=hours),
                ))
            for index, player in enumerate(players):
                for fixture in fixtures:
                    Pick.objects.create(user=player, fixture=fixture,
                                        away_pick=20 - index, home_pick=30 - index * 2)
                PlayoffPick.objects.create(
                    user=player, afc_east=teams['BUF'], afc_north=teams['BAL'],
                    afc_south=teams['HOU'], afc_west=teams['KC'],
                    nfc_east=teams['DAL'], nfc_north=teams['GB'],
                    nfc_south=teams['ATL'], nfc_west=teams['SF'],
                    sb_runner_up=teams['BUF'], sb_winner=teams['DAL'],
                )
        call_command('install_score_views', stdout=self.stdout)
        self.stdout.write(self.style.SUCCESS('Fictional demo ready.'))
        self.stdout.write('Local demo login: conorspicer / demo-only-predictor')
