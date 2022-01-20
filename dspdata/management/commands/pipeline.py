from django.core.management import BaseCommand

from dspdata.data_pipeline.email_pipeline import EmailPipeline
from dspdata.models import RawEmailData


class Command(BaseCommand):
    help = 'Starts the data pipeline'

    def handle(self, *args, **options):
        importer = EmailPipeline(RawEmailData.objects.get(pk=1))
        importer.run()