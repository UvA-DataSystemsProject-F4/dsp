import base64
import codecs
import email
import re

from dspdata.models import SubDatasource, RawEmailData


def html_to_plain(html):
    html = re.sub(r"<.*?>", "", html)  # Remove HTML tags
    html = re.sub(r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", html)  # Remove URL's
    return html


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
            return base64.b64decode(body + "===").decode('ISO-8859-1')
    else:
        if not decode_base64:
            return msg.get_payload()
        else:
            return base64.b64decode(msg.get_payload() + "===").decode('ISO-8859-1')


def extract(mail, ds, is_base64) -> RawEmailData:
    body = get_payload(mail, is_base64)
    headers_raw = dict(mail.items())
    headers_str = {str(key): str(value) for key, value in
                   headers_raw.items()}  # Fixing that some headers are not strings ?!?
    return RawEmailData(datasource=ds, headers=headers_str, subject=mail['Subject'], content_raw=body,
                        content_text=html_to_plain(body)).save()


def extract_content(mail: email.message.Message, sbs: SubDatasource):
    model = extract(mail, sbs, mail['Content-Transfer-Encoding'] is not None and "base64" in mail['Content-Transfer-Encoding'].lower())
