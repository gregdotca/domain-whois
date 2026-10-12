import pytest

import project


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(project, "sleep", lambda seconds: None)
    monkeypatch.setattr(project.whois, "whois", lambda domain: "WHOIS for " + domain)
    return project.app.test_client()


def test_root_redirects_to_default_domain(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"] == "/example.com"


def test_domain_page_shows_lookup(client):
    response = client.get("/example.com")
    assert response.status_code == 200
    assert "WHOIS for example.com" in response.get_data(as_text=True)


def test_domain_page_rejects_invalid_domain(client):
    response = client.get("/google")
    assert response.status_code == 200
    assert "Please enter a valid domain" in response.get_data(as_text=True)


@pytest.mark.parametrize("submitted, location", [
    ("example.com", "/example.com"),
    ("  bbc.co.uk  ", "/bbc.co.uk"),
    ("", "/example.com"),
])
def test_form_redirects_to_valid_domain(client, submitted, location):
    response = client.post("/", data={"domain": submitted})
    assert response.status_code == 302
    assert response.headers["Location"] == location


def test_form_redirects_idn_domain(client):
    response = client.post("/", data={"domain": "münchen.de"})
    assert response.status_code == 302
    assert client.get(response.headers["Location"]).status_code == 200


@pytest.mark.parametrize("submitted", [
    "/evil.com",
    "//evil.com",
    "https://evil.com",
    "example.com/x",
    "a?b",
    "a#b",
    "google",
])
def test_form_does_not_redirect_invalid_input(client, submitted):
    response = client.post("/", data={"domain": submitted})
    assert response.status_code == 200
    assert "Location" not in response.headers
    assert "Please enter a valid domain" in response.get_data(as_text=True)


def test_form_escapes_invalid_input(client):
    response = client.post("/", data={"domain": '"><script>x</script>'})
    body = response.get_data(as_text=True)
    assert "<script>x</script>" not in body
    assert "&lt;script&gt;" in body
