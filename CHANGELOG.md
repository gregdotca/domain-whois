# Changelog

## 2026-10-11

- Validate the domain before looking it up. `process_domain()` in `services/web/project/__init__.py` passed any text from the URL to `whois.whois()`, so things like `google` or `8.8.8.8` were sent to WHOIS servers and came back as empty results. The new `is_valid_domain()` accepts domain names, including internationalized ones like `münchen.de`, and rejects malformed punycode (`xn--`) labels. Anything else gets a "Please enter a valid domain name" message without a lookup. The form also trims spaces around the submitted domain. Update `CLAUDE.md` to match.
- Fix the Docker build's style warnings in `services/web/Dockerfile`: use `AS builder` instead of `as builder`, and `ENV KEY=value` instead of the legacy `ENV KEY value` form.
- Update `ACR.md` and the README badge from B1a to B1b, and set the `updated` date. The AI agent also wrote the domain validation, which the maintainer reviewed but didn't verify line by line, so the oversight level drops from Verified to Reviewed. The AI Share stays at 1–25%.

## 2026-10-10

- Upgrade Python from 3.9.21 to 3.14.8 in `services/web/Dockerfile`, since Python 3.9 stopped getting security updates in October 2025.
- Upgrade Flask from 2.3.0 to 3.1.3, Werkzeug from 2.3.0 to 3.1.9, and gunicorn from 20.1.0 to 26.2.0 in `services/web/requirements.txt`, to pick up their security fixes, including gunicorn's fixes for HTTP request smuggling.
- Keep python-whois at 0.8.0. The latest release, 0.9.6, looks up each TLD's WHOIS server in the IANA registry, which no longer lists one for `.uk`, so lookups like `bbc.co.uk` failed. 0.8.0 still works on Python 3.14.
- Upgrade flake8 from 3.9.1 to 7.4.1 in the Docker build, since 3.9.1 doesn't support Python 3.14.
- Start gunicorn with `--no-control-socket` in `docker-compose.yml`. gunicorn 26 opens a control socket under the app user's home directory by default, which the app user can't write to, so it logged a permission error at startup. The app doesn't use the control socket.
- Update `CLAUDE.md` with the new versions and the python-whois pin.
- Update the "How AI Was Used" section of `ACR.md` to say the AI agent also wrote these upgrades. The rating stays B1a, since the AI-written code is still under 25% of the project and the maintainer verified every line.
- Fix a cross-site scripting (XSS) hole in the lookup page. `process_domain()` in `services/web/project/__init__.py` put the raw WHOIS response into the page, and `home.html` outputs it with `|safe`, so HTML or a script in a WHOIS server's response ran in the visitor's browser. The response is now HTML-escaped before newlines are turned into `<BR>` tags. Update `CLAUDE.md` to match.
- Update `ACR.md` and the README badge from B0a to B1a, since the AI agent wrote the XSS fix, which is the first AI-written code in the project. The maintainer verified every line of it.
- Add `CLAUDE.md` with build, lint, and dev/prod switching commands and an architecture overview, so Claude Code can work in the repository without rediscovering how it's set up.
- Update the copyright notices in `LICENSE` and `README.md` to `2024-2026` and add the contact email, so they match the current year and the standard notice format.
- Fix the installation instructions in `README.md` to load the app over `http://`, since the production container serves plain HTTP on port 8094 and has no TLS.
- Add `ACR.md` with an AI Code Rating of B0a, and an ACR badge at the top of `README.md`, to disclose that the code was written without AI (an AI agent has helped only with documentation, which the rating doesn't count).
- Add this changelog.
