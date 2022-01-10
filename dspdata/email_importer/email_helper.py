import email
import json
import re

from dspdata.models import SubDatasource, RawEmailData


def html_to_plain(html):
    html = re.sub(r"<.*?>", "", html)  # Remove HTML tags
    html = re.sub(r"\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*", "", html)  # Remove URL's
    return html


def get_payload(msg):
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
                        body += get_payload(p2)

        return body
    else:
        return msg.get_payload()


def extract_plain(mail, ds) -> RawEmailData:
    body = get_payload(mail)

    headers_raw = dict(mail.items())
    headers_str = {str(key): str(value) for key, value in headers_raw.items()} # Fixing that some headers are not strings ?!?
    return RawEmailData(datasource=ds, headers=headers_str, subject=mail['Subject'], content_raw=body,
                        content_text=html_to_plain(body)).save()


def extract_base64(mail, ds) -> RawEmailData:
    pass


def extract_content(mail: email.message.Message, sbs: SubDatasource):
    if mail['Content-Transfer-Encoding'] is None:
        model = extract_plain(mail, sbs)
    elif mail['Content-Transfer-Encoding'].casefold() == "BASE64".casefold():
        model = extract_base64(mail, sbs)
    else:
        model = extract_plain(mail, sbs)