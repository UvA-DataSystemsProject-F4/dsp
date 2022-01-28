# Create your views here.
from dspdata.data_pipeline.email_pipeline import EmailPipeline
from dspdata.email_importer.email_importer import EmailImporter
from dspdata.models import RawEmailData


def loaddata_view(request):
    importer = EmailImporter("C:/Users/Jan/Projects/Python/EmailData")
    importer.execute()
    return


def pipeline_view(request):
    importer = EmailPipeline()
    importer.initialize()
    for data in RawEmailData.objects.all():
        importer.run(data)
    return
