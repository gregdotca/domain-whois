#!/usr/bin/env python3
import re
import whois
from flask import Flask, redirect, render_template, request
from markupsafe import escape
from time import sleep

app = Flask(__name__, static_folder="assets")

APP_TITLE = "Domain WHOIS Lookup"
DEFAULT_DOMAIN = "example.com"
DOMAIN_PATTERN = re.compile(
    r"(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:[a-z]{2,63}|xn--[a-z0-9-]{1,59})"
)


@app.route("/<domain>", methods=["GET"])
def home_domain(domain):
    return display_homepage(domain, process_domain(domain))


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return redirect("/" + DEFAULT_DOMAIN)
    else:
        sleep(0.25)
        submitted_domain = str(request.form["domain"]).strip()
        submitted_domain = submitted_domain or DEFAULT_DOMAIN
        return redirect("/" + submitted_domain)


def is_valid_domain(domain):
    try:
        ascii_domain = domain.encode("idna").decode("ascii")
        # decoding again rejects malformed punycode (xn--) labels
        ascii_domain.encode("ascii").decode("idna")
    except UnicodeError:
        return False

    return DOMAIN_PATTERN.fullmatch(ascii_domain.lower()) is not None


def process_domain(domain):
    page_body = ""

    if not is_valid_domain(domain):
        return "Please enter a valid domain name, such as example.com."

    try:
        domain_info = str(escape(str(whois.whois(domain))))
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
