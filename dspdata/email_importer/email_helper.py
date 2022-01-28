import base64
import email
import re

from nltk import word_tokenize
from nltk.corpus import stopwords
from spacy.lang.en import English

from dspdata.constants import words, punctuation, wordnet_lemmatizer
from dspdata.models import SubDatasource, RawEmailData

nlp = English()
nlp.add_pipe('sentencizer')


def html_to_plain(html):
    originalNLP = nlp(html)
    sentences = [sent.text.strip() for sent in originalNLP.sents]

    joined_sentence = ''.join(sentences)

    joined_sentence = re.sub(r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", joined_sentence)  # Remove URL's

    split_sentence = joined_sentence.split("\n")
    cleaned_sentence = ""
    for split in split_sentence:
        if not re.match(r"^[A-Za-z]|\s", split):
            continue  # Remove lines which do not start with text
        cleaned_sentence += split

    # Remove markup clutter
    cleaned_sentence = re.sub(r"\n", "", cleaned_sentence)
    cleaned_sentence = re.sub(r"=\d{0,3}", "", cleaned_sentence)
    cleaned_sentence = re.sub(r"&nbsp;|&rsquo;|&#39;", "", cleaned_sentence)
    cleaned_sentence = re.sub(r"\s\s+", " ", cleaned_sentence)
    cleaned_sentence = re.sub(r"\.", " ", cleaned_sentence)
    cleaned_sentence = re.sub(r"\d+", " ", cleaned_sentence)
    cleaned_sentence = re.sub(r" +", " ", cleaned_sentence)
    cleaned_sentence = re.sub(r"[^a-zA-Z]", " ", cleaned_sentence)

    # Remove non latin characters
    cleaned_sentence = re.sub(r'[^\x00-\x7f]', r'', cleaned_sentence)
    pre_processed_sentence = ""
    tokens = word_tokenize(cleaned_sentence)
    for token in tokens:
        if token.lower() not in words or not token.lower().isalpha():
            continue

        if len(token.lower()) == 1 and token.lower() not in ["a", "i"]:
            continue

        if token.lower() in stopwords.words('english'):  # Dont use stop words for final sentence
            continue

        if token in punctuation:  # Dont use punctuation for final sentence
            continue
        # stemmed = porter.stem(token) # Apply stemming
        lemmatized = wordnet_lemmatizer.lemmatize(token.lower())  # Apply lemmatization

        pre_processed_sentence += lemmatized + " "

    return pre_processed_sentence


def get_payload(msg, decode_base64=False):
    if msg.is_multipart():
        body = ""
        for payload in msg.get_payload():
            if type(payload) == str:
                body += payload
            else:
                for p2 in payload.get_payload():
                    if type(p2) == str:
                        body += p2
                    else:
                        body += get_payload(p2, decode_base64)

        if not decode_base64:
            return body
        else:
            body = body.replace('\n', '')
            if len(body) % 4:
                body += '=' * (4 - len(body) % 4)
            cleaned_sentence = re.sub(r'[^\x00-\x7f]', r'', base64.b64decode(body).decode('ISO-8859-1'))
            return cleaned_sentence
    else:
        if not decode_base64:
            return msg.get_payload()
        else:
            body = msg.get_payload()
            body = body.replace('\n', '')
            if len(body) % 4:
                body += '=' * (4 - len(body) % 4)
            cleaned_sentence = re.sub(r'[^\x00-\x7f]', r'', base64.b64decode(body).decode('ISO-8859-1'))
            return cleaned_sentence


def extract(mail, ds, is_base64):
    body = get_payload(mail, is_base64)
    plain = html_to_plain(body)
    if len(set(plain)) < 20:
        return
    headers_raw = dict(mail.items())
    headers_str = {str(key): str(value) for key, value in
                   headers_raw.items()}  # Fixing that some headers are not strings ?!?
    email_data = RawEmailData(datasource=ds, headers=headers_str, subject=mail['Subject'], content_raw=body,
                              content_text=plain)
    email_data.save()
    return email_data


def extract_content(mail: email.message.Message, sbs: SubDatasource):
    return extract(mail, sbs, mail['Content-Transfer-Encoding'] is not None and "base64" in mail[
        'Content-Transfer-Encoding'].lower())
