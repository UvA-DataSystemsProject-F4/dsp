from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from dspui import data_handler


class ApiTest(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(data=data_handler.load_by_year_month(), safe=False)


class ApiMainView(View):
    def post(self, request, *args, **kwargs):
        year_filter_start = int(request.POST.get("filter_year_start", 2018))
        year_filter_end = int(request.POST.get("filter_year_end", 2021))
        spam_filter = request.POST.get("filter_spam", 'false') == 'true'
        keyword_filter = request.POST.get("filter_keywords", "").split(",")

        return JsonResponse(data=data_handler.load_by_year_month_filter(year_filter_start, year_filter_end, spam_filter, keyword_filter), safe=False)


class ApiClusterView(View):
    def post(self, request, *args, **kwargs):
        year_filter_start = int(request.POST.get("filter_year_start", 2018))
        year_filter_end = int(request.POST.get("filter_year_end", 2021))
        spam_filter = request.POST.get("filter_spam", 'false') == 'true'
        keyword_filter = request.POST.get("filter_keywords", "").split(",")

        return JsonResponse(data=data_handler.load_cluster_data(year_filter_start, year_filter_end, spam_filter, keyword_filter), safe=False)


class ApiMonthDetailView(View):
    def post(self, request, *args, **kwargs):
        spam_filter = request.POST.get("filter_spam", 'false') == 'true'
        keyword_filter = request.POST.get("filter_keywords", "").split(",")
        month_year_filter = request.POST.get("time_step", "").split("_")

        return render(request, 'EmailResultsTable.html',
                      {'emails': data_handler.load_year_month_email_filter(month_year_filter, spam_filter, keyword_filter)
                       })
