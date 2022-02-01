import heapq

import nltk
import pandas as pd
import spacy
from nltk import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer

from dspdata.constants import wordnet_lemmatizer, list_of_scam_words
from dspdata.models import EmailDataPoint


class EmailPipeline:

    def __init__(self) -> None:
        super().__init__()
        self.email_data = None

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
            if str(twogram) not in twogram_dict.keys():
                twogram_dict[str(twogram)] = 1
            else:
                twogram_dict[str(twogram)] += 1

        # Get top 10 most frequently used two gram
        most_frequent_twograms = heapq.nlargest(10, twogram_dict, key=twogram_dict.get)

        EmailDataPoint(type=1, email=self.email_data, value=tokens).save()
        EmailDataPoint(type=2, email=self.email_data, value=bag_of_words).save()
        EmailDataPoint(type=3, email=self.email_data, value=most_frequent_words).save()
        EmailDataPoint(type=4, email=self.email_data, value=twogram_dict).save()
        EmailDataPoint(type=5, email=self.email_data, value=most_frequent_twograms).save()

    def run_tfidf(self):
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_for_all_documents = tfidf_vectorizer.fit_transform([self.email_data.content_text])
        # tfidf_for_all_documents = normalize(tfidf_for_all_documents) # Might be usefull
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()
        df_for_tfidf_in_document = pd.DataFrame(tfidf_for_all_documents[0].T.todense(), index=tfidf_feature_names,
                                                columns=["tfidf"])
        sorted_tfidf_in_document = df_for_tfidf_in_document.sort_values(by=["tfidf"], ascending=False)
        top_10_tfidf = sorted_tfidf_in_document[0:10].to_dict()["tfidf"]
        EmailDataPoint(type=20, email=self.email_data, value=top_10_tfidf).save()

    def run_named_entity(self):
        nlp = spacy.load("en_core_web_sm")
        named_entities = nlp(self.email_data.content_text)
        named_entity_list = {}
        for named_entity in named_entities.ents:
            named_entity_tuple = (named_entity.text, named_entity.label_)
            # Count named entities in the document
            if str(named_entity_tuple) not in named_entity_list.keys():
                named_entity_list[str(named_entity_tuple)] = 1
            else:
                named_entity_list[str(named_entity_tuple)] += 1
        EmailDataPoint(type=30, email=self.email_data, value=named_entity_list).save()

    def run_is_scam(self):
        EmailDataPoint(type=12, email=self.email_data, value=self.is_scam()).save()

    def is_scam(self):
        bag_of_words_dp = EmailDataPoint.objects.filter(type=2, email_id=self.email_data.id).first()
        for scam_word in list_of_scam_words:
            lem_scam_word = wordnet_lemmatizer.lemmatize(scam_word.lower())
            if scam_word in bag_of_words_dp.value or lem_scam_word in bag_of_words_dp.value:
                return True
        return False

    def run_cluster(self):
        return None

    def initialize(self):
        self.load_nltk()

    def run(self, email_data):
        self.email_data = email_data
        self.run_tokenization()
        self.run_tfidf()
        self.run_named_entity()
        self.run_is_scam()
