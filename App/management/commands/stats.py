from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help="A command to print hello "
    def handle(self, *args: Any, **options: Any) -> str | None:
        print('hello')