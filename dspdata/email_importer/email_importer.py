import email
import os
from fnmatch import fnmatch

from dspdata.email_importer.email_helper import extract_content
from dspdata.models import Datasource, SubDatasource, RawEmailData


class EmailImporter:
    def __init__(self, root_dir):
        self.root_dir = root_dir

    def execute(self):
        if Datasource.objects.filter(name="SPAM Archive").exists():
            ds = Datasource.objects.get(name="SPAM Archive")
        else:
            Datasource(name="SPAM Archive", description="Spam Archive http://untroubled.org/spam/",
                            link="http://untroubled.org/spam/").save()

        for path, subdirs, files in os.walk(self.root_dir):
            for name in files:
                if fnmatch(name, "*.txt"):
                    if SubDatasource.objects.filter(source_information=name).exists():
                        sbs = SubDatasource.objects.get(source_information=name)
                        if RawEmailData.objects.filter(datasource_id=sbs.id).exists():
                            continue
                    else:
                        SubDatasource(datasource=Datasource.objects.get(name="SPAM Archive"), source_information=name).save()
                    with open(os.path.join(path, name), "rb") as f:
                        try:
                            msg = email.message_from_binary_file(f)  # Python 3
                        except AttributeError:
                            msg = email.message_from_file(f)  # Python 2

                        extract_content(msg, SubDatasource.objects.get(source_information=name))
