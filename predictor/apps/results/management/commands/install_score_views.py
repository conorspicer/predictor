from pathlib import Path
import re

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = 'Install the original leaderboard views for MySQL or a local SQLite demo.'

    def handle(self, *args, **options):
        if connection.vendor not in {'mysql', 'sqlite'}:
            raise CommandError('Leaderboard views support MySQL and SQLite.')
        for name in ['user_scores.sql', 'user_week_results.sql']:
            sql = (Path(settings.BASE_DIR) / 'scripts' / name).read_text()
            with connection.cursor() as cursor:
                if connection.vendor == 'sqlite':
                    # Keep one scoring definition; adapt only MySQL syntax.
                    sql = re.sub(r'ISNULL\((`[^`]+`\.`[^`]+`)\)',
                                 r'(\1 IS NULL)', sql, flags=re.I)
                    sql = re.sub(r'\bNOW\(\)', 'CURRENT_TIMESTAMP', sql, flags=re.I)
                    sql = re.sub(r'\ACREATE OR REPLACE VIEW', 'CREATE VIEW',
                                 sql.strip(), flags=re.I).rstrip(';')
                    outer = re.search(r'\bAS\s*\(', sql, flags=re.I)
                    if outer:
                        sql = sql[:outer.end() - 1] + sql[outer.end():]
                        sql = sql.rstrip()[:-1]
                    view = Path(name).stem
                    cursor.execute(f'DROP VIEW IF EXISTS {connection.ops.quote_name(view)}')
                cursor.execute(sql)
            self.stdout.write(self.style.SUCCESS(f'Installed {name}'))
