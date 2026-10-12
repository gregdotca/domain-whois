import pytest

import project
from project import is_valid_domain, process_domain


@pytest.mark.parametrize("domain", [
    "example.com",
    "Example.COM",
    "www.example.com",
    "bbc.co.uk",
    "my-site.io",
    "a.co",
    "münchen.de",
    "пример.рф",
    "xn--mnchen-3ya.de",
    "xn--e1afmkfd.xn--p1ai",
])
def test_valid_domains(domain):
    assert is_valid_domain(domain)


@pytest.mark.parametrize("domain", [
    "",
    "example",
    "google",
    "8.8.8.8",
    "2001:4860:4860::8888",
    "example.c",
    "example.123",
    "example.com.",
    ".example.com",
    "example..com",
    "-example.com",
    "example-.com",
    "exa mple.com",
    "example_site.com",
    "a" * 64 + ".com",
    ("a" * 63 + ".") * 4 + "com",
    "xn--zz.com",
    "example.xn--zz",
])
def test_invalid_domains(domain):
    assert not is_valid_domain(domain)


@pytest.fixture
def lookups(monkeypatch):
    looked_up = []

    def fake_whois(domain):
        looked_up.append(domain)
        return '<script>alert("x")</script>\nline two'

    monkeypatch.setattr(project.whois, "whois", fake_whois)
    return looked_up


def test_invalid_domain_skips_lookup(lookups):
    assert process_domain("google").startswith("Please enter a valid domain")
    assert lookups == []


def test_result_is_escaped(lookups):
    assert process_domain("example.com") == (
        "&lt;script&gt;alert(&#34;x&#34;)&lt;/script&gt;<BR>line two"
    )


@pytest.mark.parametrize("domain, expected", [
    ("example.com", "example.com"),
    ("münchen.de", "münchen.de"),
    ("xn--mnchen-3ya.de", "münchen.de"),
    ("xn--e1afmkfd.xn--p1ai", "пример.рф"),
])
def test_punycode_is_looked_up_in_unicode(lookups, domain, expected):
    process_domain(domain)
    assert lookups == [expected]


def test_lookup_error_shows_message(monkeypatch):
    def failing_whois(domain):
        raise OSError("connection refused")

    monkeypatch.setattr(project.whois, "whois", failing_whois)
    assert process_domain("example.com").startswith("Unable to perform")
