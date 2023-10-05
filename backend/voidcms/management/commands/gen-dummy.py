# File: generate_dummy_data.py

from django.core.management.base import BaseCommand
from voidcms.faker.genDummy import generate_dummy_data


class Command(BaseCommand):
    help = 'Generate dummy data for categories and products'

    def handle(self, *args, **kwargs):
        self.stdout.write('Generating dummy data...')
        generate_dummy_data()
        self.stdout.write(self.style.SUCCESS(
            'Dummy data generated successfully.'))
