# Generated by Django 3.2.11 on 2022-01-24 14:24

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dspdata', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaildatapoint',
            name='value',
            field=jsonfield.fields.JSONField(blank=True, null=True),
        ),
    ]