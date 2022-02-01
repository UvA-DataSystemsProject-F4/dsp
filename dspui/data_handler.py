from django.db.models import Q

from dspdata.models import RawEmailData, EmailDataPoint

Month_Short = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_by_year_month():
    results = {}
    for year in [2018, 2019, 2020]:
        for month in range(0, 12):
            results[f'{Month_Short[month]}_{year}'] = RawEmailData.objects.filter(
                headers__contains=f"{Month_Short[month]} {year}").count()

    return {
        'labels': list(results.keys()),
        'datasets': [
            {
                'label': "Amount Found",
                'data': list(results.values()),
            },
        ]
    }


def query_spam(filter_spam):
    if filter_spam:
        return Q(type=12, value=True)
    else:
        return Q()


def query_keyword(filter_keyword):
    query = Q()
    for keyword in filter_keyword:
        query = query | Q(email__content_text__contains=keyword)
    return query


def load_by_year_month_filter(filter_year_start, filter_year_end, filter_spam, filter_keywords):
    results = {}
    for filter_year in range(filter_year_start, filter_year_end + 1):
        for month in range(0, 12):
            results[f'{Month_Short[month]}_{filter_year}'] = EmailDataPoint.objects \
                .filter(query_spam(filter_spam)) \
                .filter(email__headers__contains=f"{Month_Short[month]} {filter_year}") \
                .filter(query_keyword(filter_keywords)) \
                .values('email') \
                .distinct() \
                .count()

    return {
        'labels': list(results.keys()),
        'datasets': [
            {
                'label': "Amount Found",
                'data': list(results.values()),
            },
        ]
    }
