from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = 'Create or replace the leaderboard SQL views in the configured MySQL database.'

    def handle(self, *args, **options):
        if connection.vendor != 'mysql':
            raise CommandError('The leaderboard SQL views require MySQL.')
        for name in ['user_scores.sql', 'user_week_results.sql']:
            sql = (Path(settings.BASE_DIR) / 'scripts' / name).read_text()
            with connection.cursor() as cursor:
                cursor.execute(sql)
            self.stdout.write(self.style.SUCCESS(f'Installed {name}'))
