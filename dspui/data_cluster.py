from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE


def create_tfidf(document_list):
    return TfidfVectorizer(smooth_idf=True, norm='l2').fit_transform(document_list)


def create_plot_cluster(tfidf):
    model = KMeans(35)
    model.fit(tfidf)

    tfs_reduced = TruncatedSVD(n_components=35, random_state=42).fit_transform(tfidf)
    tfs_embedded = TSNE(n_components=2, perplexity=40, verbose=2).fit_transform(tfs_reduced)

    datasets = {}
    for i in range(len(tfs_embedded)):
        key = f'{model.labels_[i]}'
        if key not in datasets:
            datasets[key] = {
                'label': key,
                'data': []
            }

        datasets[key]['data'].append({
            'x': float(tfs_embedded[i, 0]),
            'y': float(tfs_embedded[i, 1]),
        })
    return datasets, model.labels_
