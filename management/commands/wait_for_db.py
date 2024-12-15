import time
from sqlite3 import OperationalError

from django.core.management import BaseCommand
from psycopg2.errors import OperationalError as PsycopgError
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_check = False

        while db_check is False:
            try:
                self.check(databases=["default"])
                db_check = True
            except (PsycopgError, OperationalError):
                self.stdout.write(self.style.ERROR('Database is not ready'))
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database is ready'))
