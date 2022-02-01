import email
import io
import os
from fnmatch import fnmatch

from tqdm import tqdm

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
        count = 0
        count2 = 0
        for path, subdirs, files in tqdm(list(os.walk(self.root_dir))):
            count += 1
            if count < 19:
                continue
            for name in tqdm(files):
                count2 += 1
                if count2 < 103563:
                    continue
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

                        try:
                            extract_content(msg, SubDatasource.objects.get(source_information=name))
                        except Exception as err:
                            with io.open("MalformedEmails.txt", "a") as err_file:
                                err_file.write(os.path.join(path, name) + "\n")
                            with io.open("MalformedErrors.txt", "a") as err_file:
                                if hasattr(err, 'message'):
                                    err_file.write(err.message + "\n")
                                else:
                                    err_file.write(str(err) + "\ n")