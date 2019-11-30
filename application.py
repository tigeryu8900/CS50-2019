import cs50
import re
import requests
from flask import Flask, abort, redirect, render_template, make_response, request, jsonify
from html import escape
from werkzeug.exceptions import default_exceptions, HTTPException

from helpers import *

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """ Disable caching """
    #response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #response.headers["Expires"] = 0
    #response.headers["Pragma"] = "no-cache"
    return response


@app.route('/', defaults={'url': ''})
@app.route('/proxy', defaults={'url': ''})
@app.route("/<path:url>")
def root(url):
    """Handle requests for / via GET (and POST)"""
    print(f"root url: {url}")
    target = request.args.get("site", None)
    if target is None:
        target = request.headers.get('referer')
    if target:
        redirect_url = getProxiedUrl(target)
        print(f"root redirect to {redirect_url}")
        return redirect(redirect_url)
    return render_template("proxy.html", name=url, request=request)


@app.route("/proxy/<path:url>", methods=["GET", "POST"])
def proxy(url):
    """Handle requests for /proxy"""
    print(f"route url: {url}")
    #print(f"request.args: {request.args}")
    # return error(f"the method {request.method} is not yet supported", 405)
    if request.method == "GET":
        return doGet(url)
    elif request.method == "POST":
        return doPost(url)
    else:
        return error(f"the method {request.method} is not yet supported", 405)


@app.route("/error", methods=["GET", "POST"])
def get_error():
    return error()


@app.errorhandler(HTTPException)
def errorhandler(error):
    """ Handle errors """
    return error(error.description, error.code)


def getProxiedUrl(url):
    if url.find("/proxy/") >= 0:
        return url
    if url.startswith("http://") or url.startswith("https://"):
        return "/proxy/" + url
    return "/proxy/http://" + url


# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

