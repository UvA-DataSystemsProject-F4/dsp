from django.db import models
from jsonfield import JSONField


class Datasource(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=2560)
    link = models.CharField(max_length=1024)


class SubDatasource(models.Model):
    datasource = models.ForeignKey(Datasource, on_delete=models.DO_NOTHING, related_name='children')
    source_information = models.CharField(max_length=1024)


class RawEmailData(models.Model):
    datasource = models.ForeignKey(SubDatasource, on_delete=models.DO_NOTHING, related_name='data')
    headers = JSONField(null=True, blank=True)
    subject = models.TextField(null=True, blank=True)
    content_raw = models.TextField(null=True, blank=True)
    content_text = models.TextField(null=True, blank=True)


class EmailDataPoint(models.Model):
    TYPE_CHOICES = (
        (1, 'NamedEntity'),
        (2, 'ExternalReference'),
        (3, 'Other'),

    )
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, blank=True, null=True)
    email = models.ForeignKey(RawEmailData, on_delete=models.DO_NOTHING, related_name='datapoints')
    value = models.TextField()
