#!/usr/bin/env python3
import whois
from flask import Flask, render_template, request
from time import sleep

app = Flask(__name__, static_folder="assets")

APP_TITLE = "Domain WHOIS Lookup"


@app.route("/<domain>", methods=["GET"])
def home_domain(domain):
    return display_homepage(domain, process_domain(domain))


@app.route("/", methods=["GET"])
def home():
    domain = "example.com"
    page_body = process_domain(domain)

    return display_homepage(domain, page_body)


@app.route("/", methods=["POST"])
def home_post():
    domain = "example.com"

    sleep(0.25)

    submitted_domain = str(request.form["domain"])

    if submitted_domain == "":
        submitted_domain = domain

    page_body = process_domain(submitted_domain)

    return display_homepage(submitted_domain, page_body)


def process_domain(domain):
    page_body = ""

    try:
        domain_info = str(whois.whois(domain))
        domain_info = domain_info.replace("\n", "<BR>")

        page_body += domain_info

    except Exception:
        page_body += "Unable to perform domain WHOIS lookup, please try again."

    return page_body


def display_homepage(domain, page_body):
    return render_template(
        "home.html", app_title=APP_TITLE, domain=domain, page_body=page_body
    )


if __name__ == "__main__":
    app.run()
