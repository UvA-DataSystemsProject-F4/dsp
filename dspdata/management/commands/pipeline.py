from django.core.management import BaseCommand
from tqdm import tqdm

from dspdata.data_pipeline.email_pipeline import EmailPipeline
from dspdata.models import RawEmailData


class Command(BaseCommand):
    help = 'Starts the data pipeline'

    def handle(self, *args, **options):
        importer = EmailPipeline()
        importer.initialize()
        for data in tqdm(RawEmailData.objects.all()):
            if data.id >= 46269:
                importer.run(data)
