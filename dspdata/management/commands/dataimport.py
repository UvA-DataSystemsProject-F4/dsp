from django.core.management import BaseCommand

from dspdata.email_importer.email_importer import EmailImporter


class Command(BaseCommand):
    help = 'Starts the importing of data files'

    def add_arguments(self, parser):
        parser.add_argument('dir', type=str)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f'Starting import of directory: {options["dir"]}'))
        importer = EmailImporter(options["dir"])
        importer.execute()

