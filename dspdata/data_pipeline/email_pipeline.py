import heapq

import nltk
import pandas as pd
import spacy
from nltk import ngrams

from sklearn.feature_extraction.text import TfidfVectorizer

from dspdata.models import RawEmailData


class EmailPipeline:

    def __init__(self, email_data: RawEmailData) -> None:
        super().__init__()
        self.email_data = email_data

    def load_nltk(self):
        nltk.download('stopwords')
        nltk.download('omw-1.4')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        nltk.download('words')
        nltk.download('brown')
        nltk.download('punkt')

    def run_tokenization(self):
        bag_of_words = {}

        tokens = nltk.word_tokenize(self.email_data.content_text)

        for token in tokens:
            if token not in bag_of_words.keys():
                bag_of_words[token] = 1
            else:
                bag_of_words[token] += 1

        # Get the 10 most frequently used words in a document
        most_frequent_words = heapq.nlargest(10, bag_of_words, key=bag_of_words.get)

        # Get n-grams from document
        twograms = ngrams(tokens, 2)

        twogram_dict = {}

        for twogram in twograms:
            if twogram not in twogram_dict.keys():
                twogram_dict[twogram] = 1
            else:
                twogram_dict[twogram] += 1

        # Get top 10 most frequently used two gram
        most_frequent_twograms = heapq.nlargest(10, twogram_dict, key=twogram_dict.get)
        print(most_frequent_twograms)

    def run_tfidf(self):
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_for_all_documents = tfidf_vectorizer.fit_transform([self.email_data.content_text])
        # tfidf_for_all_documents = normalize(tfidf_for_all_documents) # Might be usefull
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()
        df_for_tfidf_in_document = pd.DataFrame(tfidf_for_all_documents[0].T.todense(), index=tfidf_feature_names,
                                                columns=["tfidf"])
        sorted_tfidf_in_document = df_for_tfidf_in_document.sort_values(by=["tfidf"], ascending=False)
        top_10_tfidf = sorted_tfidf_in_document[0:10].to_dict()["tfidf"]
        print(top_10_tfidf)

    def run_named_entity(self):
        nlp = spacy.load("en_core_web_sm")
        named_entities = nlp(self.email_data.content_text)
        named_entity_list = {}
        for named_entity in named_entities.ents:
            named_entity_tuple = (named_entity.text, named_entity.label_)
            # Count named entities in the document
            if named_entity_tuple not in named_entity_list.keys():
                named_entity_list[named_entity_tuple] = 1
            else:
                named_entity_list[named_entity_tuple] += 1

    def cluster(self):
        return None

    def run(self):
        self.load_nltk()
        self.run_tokenization()
        self.run_tfidf()
        self.run_named_entity()
