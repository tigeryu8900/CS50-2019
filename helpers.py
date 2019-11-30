import os
import requests
import urllib.parse
import re
import pickle

from flask import redirect, render_template, request, session, make_response
from functools import wraps
from urllib.parse import urlparse

def error(message="that page doesn't exist", code=400):
    """Render message as an apology to user."""
    return render_template("error.html", code=code, message=message), code


formattingRegex = {
    "text": [
        # (re.compile("(?<=('|\"))([\\./].*?[^\\\\](?:\\\\\\\\)*)(?=\\1)"), "/proxy/{}\\2")
        # (re.compile("(?<=('|\"))([\\./].*?[^\\\\](?:\\\\\\\\)*)(?=\\1)"), "/proxy/{}\\2")
        # (re.compile("(?<=('|\"))((?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*)(?=\\1)"), "/proxy/{}\\2")
        # (re.compile("(?<=('|\"))([^www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//].*?[^\\\\](?:\\\\\\\\)*)(?=\\1)"), "/proxy/{}\\2")
        # (re.compile("(?<=('|\"))([^(?:(?:http|ftp)s?)].*?[^\\\\](?:\\\\\\\\)*)(?=\\1)"), "/proxy/{}\\2"),
        # (re.compile("(?<=('|\"))((?:(?:http|ftp)s?).*?[^\\\\](?:\\\\\\\\)*)(?=\\1)"), "/proxy/\\2")
    ],
    "text/html": [
        (re.compile("(?=<head>)"), '<script src="/proxy/https://unpkg.com/xhook@latest/dist/xhook.min.js"></script><script src="/proxy/https://cdn.jsdelivr.net/npm/jquery/dist/jquery.min.js"></script><script src="https://cdn.jsdelivr.net/npm/js-cookie/dist/js.cookie.min.js"></script></script><script src="/static/request_capture.js"></script>', 1)
        # (re.compile("(?<=('|\"))((?:(?:http|ftp)s?).*?[^\\\\](?:\\\\\\\\)*)(?=\\1)"), "/proxy/\\2")
    ],
    "application/javascript": [
        # (re.compile("(?<=('|\"))([^www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//].*?[^\\\\](?:\\\\\\\\)*)(?=\\1)"), "/proxy/{}\\2")
    ]
}

def getCookieKey(url):
    return "__cookies_" + urlparse(url).netloc

def getCookiesToSend(url):
    """ get the pickled cookiejar for the given host, returns the unpacked cookiejar """
    return request.cookies
    cookie_bytes = bytes.fromhex(request.cookies.get(getCookieKey(url), ""))
    if len(cookie_bytes) > 0:
        return pickle.loads(cookie_bytes)
    else:
        return dict()

def handleResponseCookies(response):
    """ pickle the cookiejar in response and save it as whole in response again """
    cookie_str = pickle.dumps(response.cookies).hex()
    return cookie_str

def doGet(url):
    response = requests.get(url, params=request.args, headers={"User-Agent": request.headers.get("User-Agent")}, cookies=getCookiesToSend(url))
    return formatResponse(response, url)

def doPost(url):
    response = requests.post(url, data=request.form, headers={"User-Agent": request.headers.get("User-Agent")}, cookies=getCookiesToSend(url))
    return formatResponse(response, url)


def formatResponse(response, url):
    html = None
    data = response.content
    t = response.headers.get("Content-Type")
    # print(f"headers: {response.headers}")
    print(f"content type: {t}")
    for key in formattingRegex:
        if t.find(key) > -1:
            # print(">>>>> Content is html!")
            html = response.text
            for reg in formattingRegex[key]:
                # print(f"reg: {reg}")
                # print(f"find: {reg[0]} replace: {reg[1].format(url)}")
                if (len(reg) == 2):
                    html = reg[0].sub(reg[1].format(url), html)
                elif (len(reg) == 3):
                    html = reg[0].sub(reg[1].format(url), html, reg[2])
            data = html.encode()

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]
    result = make_response(data, response.status_code, headers)
#    result.set_cookie(getCookieKey(url), handleResponseCookies(response))
    return result
