import csv
from django.core.management.base import BaseCommand
from catalog.models import Star

class Command(BaseCommand):
    help = 'Load stars from hipparcos_sample.csv'

    def handle(self, *args, **kwargs):
        with open('hipparcos_sample.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Star.objects.get_or_create(
                    name=row['name'],
                    constellation=row['constellation'],
                    magnitude=row['magnitude'],
                    ra=row['ra'],
                    dec=row['dec']
                )
        self.stdout.write(self.style.SUCCESS('Star data imported successfully.'))
