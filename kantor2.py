import requests
import csv
from flask import Flask, render_template, request, redirect

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0].get("rates")

app = Flask(__name__)


def get_codes():
    codes = []
    for data in rates:
        codes.append(data.get("code"))
    return sorted(codes)


codes = get_codes()

with open("rates.csv", "w") as csvfile:
    fieldnames = ["currency", "code", "bid", "ask"]
    writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rates)


@app.route("/kantor/", methods=["GET", "POST"])
def message():
    if request.method == "POST":
        data = request.form
        currency = data.get("code")
        amount = data.get("amount")
        ask = data.get("ask")
        # score = ask*amount
        return f"{data}{currency}{ask} ,kosztuje  PLN"
    return render_template("templates.html", codes=codes)
