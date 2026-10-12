# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A single-page Flask app that runs a WHOIS lookup on a domain and shows the raw result. The live demo is https://whois.greg.ca. All the app code is in `services/web/project/__init__.py` and `services/web/project/templates/home.html`.

## Commands

Each command block below starts from the repository root and leaves you there.

Production (the tracked `docker-compose.yml`), served by gunicorn on host port 8094:

```bash
docker compose up -d --build
```

Tests live in `services/web/tests/` and cover `is_valid_domain()` and `process_domain()`, with `whois.whois()` stubbed out so they need no network. The production Docker build runs them after flake8, so a failing test fails the build. pytest isn't in `requirements.txt`; to run the tests locally, use `python -m`, so `project` is importable. The maintainer's working copy has a gitignored `.venv` at the repository root with the requirements, pytest, and flake8 installed; in a fresh clone, create one first:

```bash
python3 -m venv .venv && .venv/bin/pip install -r services/web/requirements.txt pytest==9.1.1 flake8==7.4.1
source .venv/bin/activate
(cd services/web && python -m pytest)
```

Linting runs inside the production Docker build, so a flake8 error fails the build. flake8 isn't in `requirements.txt`; to run the same check locally, install the version the Dockerfile pins:

```bash
pip install flake8==7.4.1
(cd services/web && flake8 --ignore=E501,W503,F401 .)
```

`requirements.txt` pins the indirect dependencies too (Jinja2, MarkupSafe, and so on), so rebuilds are repeatable; when upgrading a package, update any indirect pins it needs. The Dockerfile also pins the base image, `python:3.14.8-slim`, and builds the CSS (see Frontend below). To build the CSS outside Docker, install the Tailwind standalone CLI at the version the Dockerfile pins:

```bash
(cd services/web && tailwindcss -i project/styles/app.css -o project/assets/app.css --watch)
```

### Dev/prod switching

The dev setup lives in files that are excluded locally through `.git/info/exclude` (`docker-compose.DEV.yml`, `services/web/Dockerfile.DEV`, `to-dev.sh`, `to-prod.sh`, `test.py`). They exist only in the maintainer's working copy; a fresh clone has just the production setup, and this section doesn't apply to it. `./to-dev.sh` and `./to-prod.sh` swap environments by **renaming** files: the active pair is always `docker-compose.yml` and `services/web/Dockerfile`, and the inactive pair gets a `.PROD` or `.DEV` suffix. In dev, the app runs with the Flask debug server on port 5000 (`python manage.py --debug run -h 0.0.0.0`, which also works from `services/web/` with the local `.venv`), and `services/web/` is bind-mounted into the container. Alongside it, `tailwindcss --watch=always` rebuilds `project/assets/app.css` into the mounted directory (`--watch=always` because the container's stdin is closed), so the file on the host is owned by root. `Dockerfile.DEV` pins the same `python:3.14.8-slim` base image and Tailwind CLI, so upgrading either one has to change both Dockerfiles. It doesn't run flake8, so lint errors only show up in a production build.

Because the tracked files are the production ones, run `./to-prod.sh` before committing. Otherwise git sees the dev files in place of the production `docker-compose.yml` and `Dockerfile`. `test.py` is a scratch script that doesn't relate to the app.

## Architecture

- **Routes:** `GET /<domain>` does the lookup and renders the page. `GET /` redirects to `/example.com`. `POST /` (the form) sleeps 0.25s so the loading spinner shows, then redirects to `/<submitted domain>`. Every lookup is a GET to a shareable URL.
- **Lookup:** `process_domain()` first checks the domain with `is_valid_domain()`, which converts it to ASCII with the `idna` codec (so internationalized names work), decodes it back to reject malformed punycode (`xn--`) labels, and matches it against `DOMAIN_PATTERN`. Anything else, including IP addresses and bare words, gets a fixed message without a lookup. Valid domains go to `whois.whois()` from `python-whois` in Unicode form (`domain.encode("idna").decode("idna")`), never the ASCII form that was validated: python-whois matches the public suffix list, which stores IDN suffixes in Unicode, so `xn--e1afmkfd.xn--p1ai` would be looked up as just the TLD and come back empty. Then `process_domain()` turns newlines in the result into `<BR>`. Any exception becomes a generic error message. `python-whois` is deliberately kept at 0.8.0: 0.9.x finds WHOIS servers through the IANA registry, which lists none for `.uk`, so `.uk` lookups fail. Check `.uk` and a few other TLDs before upgrading it.
- **Rendering:** `home.html` outputs `page_body` with `|safe`, because `process_domain()` adds the `<BR>` tags itself. The WHOIS response is untrusted, so `process_domain()` HTML-escapes it with `markupsafe.escape` first. Any new text that goes into `page_body` must be escaped the same way.
- **Frontend:** Tailwind 4 and daisyUI 5 are built at Docker build time, not loaded from a CDN. The Tailwind standalone CLI (version and per-architecture SHA-256s pinned as `ARG`s in the Dockerfile's builder stage) compiles `project/styles/app.css` into `project/assets/app.css`, which is gitignored and copied into the final stage. `app.css` uses `source(none)` and `@source "../templates"`, so only the templates are scanned: a class used only from Python or JS won't be in the build unless it also appears in a template. daisyUI is the vendored plugin `project/styles/daisyui-<version>.mjs`, with only the `bumblebee` (light) and `business` (dark) themes enabled. To upgrade, change the Dockerfile `ARG`s (and `Dockerfile.DEV`'s), or replace the `.mjs` file and its reference in `app.css`. The favicon is served locally from `project/assets/`, which is Flask's `static_folder`, at `/assets/...` (use `url_for('static', ...)`). There's no JavaScript library: the only script is the Lookup button's inline `onclick`, which shows the loading spinner. The page has a doctype, `lang="en"`, and a viewport meta tag, so it renders in standards mode and at phone width.
- **Dark mode:** automatic only, with no toggle, JavaScript, or `data-theme` attribute. `bumblebee --default, business --prefersdark` in `project/styles/app.css` puts `business` inside `@media (prefers-color-scheme: dark)` on `:root:not([data-theme])`, so adding `data-theme` to `<html>` would lock the page to one theme. A `color-scheme` meta tag at the top of `<head>` tells the browser about both modes before the CSS loads. Use daisyUI theme colours (`base-content`, `base-200`, and so on), not hard-coded colour classes (`text-gray-*`, `bg-white`), so both modes keep working. Tailwind's `dark:` variant uses the same media query, so per-mode tweaks go there (the Lookup button is `btn-accent dark:btn-primary`, since `business`'s accent is orange). Dark-mode overrides of theme variables live in an unlayered rule at the end of `app.css`: a darker `--color-primary` for the button, and `bumblebee`'s `--radius-*` corner sizes so both modes match. Being unlayered, it beats daisyUI's theme in `@layer base`.
- **Custom headers:** `home.html` includes `templates/custom.headers` if it exists (`ignore missing`). The file is gitignored and holds deployment-specific `<head>` content.
- `manage.py` wraps the app in a `FlaskGroup` CLI. gunicorn loads `manage:app`.
