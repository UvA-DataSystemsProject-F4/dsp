# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from dspdata.models import Datasource, SubDatasource, RawEmailData, EmailDataPoint


class IndexView(TemplateView):
    template_name = "Index.html"


class DatasourceView(View):
    def get(self, request, *args, **kwargs):
        if 'id' not in kwargs:
            return render(request, 'DataSourceView.html', {'sources': Datasource.objects.all()})

        return render(request, 'DataSourceView.html', {'source': Datasource.objects.get(pk=kwargs['id']),
                                                       'subsources': SubDatasource.objects.all()[:100]})


class SubDatasourceView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'SubDatasourceView.html',
                      {'object': get_object_or_404(RawEmailData, pk=kwargs['id'])
                       })


class EmailDataPointsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'SubDatasourceView.html',
                      {'datapoints': EmailDataPoint.objects.filter(email_id=kwargs['id'])
                       })
