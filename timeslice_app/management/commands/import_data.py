import csv
from django.core.management.base import BaseCommand
from timeslice_app.models import TimeSlice
from datetime import datetime

class Command(BaseCommand):
    help = 'Import magic time clips from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['csv_file']
        count = 0

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    TimeSlice.objects.create(
                        title=row['title'],
                        description=row['description'],
                        historical_date=datetime.strptime(row['historical_date'], '%Y-%m-%d').date(),
                        location=row['location'],
                        category=row['category'],
                        price=round(10 + 30 * count / 2000, 2),
                        image_url=row['image_url']
                    )
                    count += 1
                except Exception as e:
                    self.stderr.write(f"Import failed: {row}\nError: {e}")

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} magic time clips! '
))
