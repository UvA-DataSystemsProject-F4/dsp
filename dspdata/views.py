# Create your views here.
from dspdata.email_importer.email_importer import EmailImporter


def loaddata_view(request):
    importer = EmailImporter("C:/Users/Jan/Projects/Python/EmailData")
    importer.execute()
    return
