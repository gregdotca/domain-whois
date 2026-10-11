# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A single-page Flask app that runs a WHOIS lookup on a domain and shows the raw result. The live demo is https://whois.greg.ca. All the app code is in `services/web/project/__init__.py` and `services/web/project/templates/home.html`.

## Commands

Production (the tracked `docker-compose.yml`), served by gunicorn on host port 8094:

```bash
docker compose up -d --build
```

There are no tests. Linting runs inside the production Docker build, so a flake8 error fails the build. flake8 isn't in `requirements.txt`; to run the same check locally, install the version the Dockerfile pins:

```bash
pip install flake8==3.9.1
cd services/web && flake8 --ignore=E501,W503,F401 .
```

The Dockerfile also pins the base image, `python:3.9.21-slim`.

### Dev/prod switching

The dev setup lives in files that are excluded locally through `.git/info/exclude` (`docker-compose.DEV.yml`, `services/web/Dockerfile.DEV`, `to-dev.sh`, `to-prod.sh`, `test.py`). They exist only in the maintainer's working copy; a fresh clone has just the production setup, and this section doesn't apply to it. `./to-dev.sh` and `./to-prod.sh` swap environments by **renaming** files: the active pair is always `docker-compose.yml` and `services/web/Dockerfile`, and the inactive pair gets a `.PROD` or `.DEV` suffix. In dev, the app runs with the Flask debug server on port 5000, and `services/web/` is bind-mounted into the container.

Because the tracked files are the production ones, run `./to-prod.sh` before committing. Otherwise git sees the dev files in place of the production `docker-compose.yml` and `Dockerfile`. `test.py` is a scratch script that doesn't relate to the app.

## Architecture

- **Routes:** `GET /<domain>` does the lookup and renders the page. `GET /` redirects to `/example.com`. `POST /` (the form) sleeps 0.25s so the loading spinner shows, then redirects to `/<submitted domain>`. Every lookup is a GET to a shareable URL.
- **Lookup:** `process_domain()` calls `whois.whois()` from `python-whois` and turns newlines into `<BR>`. Any exception becomes a generic error message.
- **Rendering:** `home.html` outputs `page_body` with `|safe`, because `process_domain()` adds the `<BR>` tags itself. The WHOIS response is untrusted, so `process_domain()` HTML-escapes it with `markupsafe.escape` first. Any new text that goes into `page_body` must be escaped the same way.
- **Frontend:** Tailwind v4 (browser build) and daisyUI 5 come from the jsDelivr CDN (theme `bumblebee`). jQuery 3.7.1 and the favicon are served locally from `project/assets/`, which is Flask's `static_folder`.
- **Custom headers:** `home.html` includes `templates/custom.headers` if it exists (`ignore missing`). The file is gitignored and holds deployment-specific `<head>` content.
- `manage.py` wraps the app in a `FlaskGroup` CLI. gunicorn loads `manage:app`.
