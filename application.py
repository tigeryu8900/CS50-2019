import cs50
import csv
import re

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get("name", "")
    house = request.form.get("house", "")
    position = request.form.get("position", "")
    if name == "":
        return render_template("error.html", message="You must specify your name.")

    if house == "":
        return render_template("error.html", message="You must specify your house.")

    if position == "":
        return render_template("error.html", message="You must specify your position.")

    csv.writer(open('survey.csv', 'a')).writerow([name, house, position])

    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    datastr = str(list(csv.reader(open('survey.csv'))))
    # datastr = re.sub("\\A\\[", "", datastr)
    # datastr = re.sub("\\]\\Z", "", datastr)
    # datastr = re.sub("\\[", "<tr>", datastr)
    # datastr = re.sub("\\]", "</tr>", datastr)
    # datastr = re.sub("(?:\"(.*?)\")|(?:'(.*?)')", "<td>\\1\\2</td>", datastr)
    # datastr = re.sub(",", "\n", datastr)
    return render_template("sheet.html", data=datastr)
