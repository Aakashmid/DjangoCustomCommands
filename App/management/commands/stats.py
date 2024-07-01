from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help="A command to print hello "
    def handle(self, *args: Any, **options: Any) -> str | None:
        import os
        from django.conf import settings

        # Get the base directory of the project
        base_dir = settings.BASE_DIR

        # Construct the path to the settings.py file
        settings_file_path = os.path.join(base_dir, 'path', 'to', 'settings.py')

        print(f'The path to the settings.py file is: {settings_file_path}')