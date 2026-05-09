from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from django.db import transaction


class Command(BaseCommand):
    help = 'Загрузка фикстур из папки data/fixtures в указанном порядке'

    def handle(self, *args, **kwargs):
        # Путь к папке с фикстурами
        fixtures_dir = os.path.join('data', 'fixtures')

        # Порядок файлов
        fixture_files = [
            'keywords.json',
            'instruments.json',
            'line_up.json',
            'lineupcomposition.json',
            'event.json',
            'video.json',
        ]

        # Загружаем фикстуры по очереди
        with transaction.atomic():
            for fixture in fixture_files:
                fixture_path = os.path.join(fixtures_dir, fixture)
                if os.path.exists(fixture_path):
                    self.stdout.write(f'Загружаю {fixture}...')
                    call_command('loaddata', fixture_path)
                else:
                    self.stdout.write(f'Файл {fixture} не найден в {fixtures_dir}')