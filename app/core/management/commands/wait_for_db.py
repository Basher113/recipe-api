"""
Django command to wait for the database to be available.
"""

from django.core.management.base import BaseCommand, CommandError
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
import time

class Command(BaseCommand):
    """Django command to wait"""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for db')
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database not ready, waiting 1 second.')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database is available! ✅"))
