# Changelog

## 2026-10-10

- Fix a cross-site scripting (XSS) hole in the lookup page. `process_domain()` in `services/web/project/__init__.py` put the raw WHOIS response into the page, and `home.html` outputs it with `|safe`, so HTML or a script in a WHOIS server's response ran in the visitor's browser. The response is now HTML-escaped before newlines are turned into `<BR>` tags. Update `CLAUDE.md` to match.
- Update `ACR.md` and the README badge from B0a to B1a, since the AI agent wrote the XSS fix, which is the first AI-written code in the project. The maintainer verified every line of it.
- Add `CLAUDE.md` with build, lint, and dev/prod switching commands and an architecture overview, so Claude Code can work in the repository without rediscovering how it's set up.
- Update the copyright notices in `LICENSE` and `README.md` to `2024-2026` and add the contact email, so they match the current year and the standard notice format.
- Fix the installation instructions in `README.md` to load the app over `http://`, since the production container serves plain HTTP on port 8094 and has no TLS.
- Add `ACR.md` with an AI Code Rating of B0a, and an ACR badge at the top of `README.md`, to disclose that the code was written without AI (an AI agent has helped only with documentation, which the rating doesn't count).
- Add this changelog.
