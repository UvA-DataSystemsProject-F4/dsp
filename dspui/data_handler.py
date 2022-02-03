from django.db.models import Q

from dspdata.models import RawEmailData, EmailDataPoint
from dspui import data_cluster

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


def query_time(year_start, year_end):
    query = Q()
    for filter_year in range(year_start, year_end + 1):
        for month in range(0, 12):
            query = query | Q(email__headers__contains=f"{Month_Short[month]} {filter_year}")
    return query


def load_by_year_month_filter(filter_year_start, filter_year_end, filter_spam, filter_keywords):
    results = {}
    for filter_year in range(filter_year_start, filter_year_end + 1):
        for month in range(0, 12):
            results[f'{Month_Short[month]}_{filter_year}'] = EmailDataPoint.objects \
                .filter(query_spam(filter_spam)) \
                .filter(email__headers__contains=f"{Month_Short[month]} {filter_year}") \
                .filter(query_keyword(filter_keywords)) \
                .order_by('email') \
                .values_list('email', flat=True) \
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


def load_cluster_data(filter_year_start, filter_year_end, filter_spam, filter_keywords):
    email_ids = EmailDataPoint.objects \
        .filter(query_spam(filter_spam)) \
        .filter(query_time(filter_year_start, filter_year_end)) \
        .filter(query_keyword(filter_keywords)) \
        .order_by('email') \
        .values_list('email', flat=True) \
        .distinct()
    strings_id = RawEmailData.objects.filter(id__in=email_ids).values_list('content_text', 'id')
    tfidf = data_cluster.create_tfidf([x[0] for x in strings_id])
    datasets, labels = data_cluster.create_plot_cluster(tfidf)
    return {
        'plotting': {
            'datasets': list(datasets.values())
        },
        'clusterData': {
            'labels': labels.tolist(),
            'data': list([x[0] for x in strings_id]),
            'id': [x[1] for x in strings_id]
        }
    }


def load_year_month_email_filter(time_step, filter_spam, filter_keywords):
    email_ids = EmailDataPoint.objects \
        .filter(query_spam(filter_spam)) \
        .filter(email__headers__contains=f"{time_step[0]} {time_step[1]}") \
        .filter(query_keyword(filter_keywords)) \
        .order_by('email') \
        .values_list('email', flat=True) \
        .distinct()

    return RawEmailData.objects.filter(id__in=email_ids)
