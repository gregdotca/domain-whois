---
rating: B1b
spec: "0.1"
updated: 2026-10-11
---

# AI Code Rating

**ACR B1b** (Maintainer: Experienced · AI Share: 1–25% · Oversight: Reviewed)

This project is rated with [AI Code Rating](https://aicoderating.com/spec/0.1/), spec version 0.1.

## How AI Was Used

The maintainer wrote nearly all of Domain WHOIS Lookup's code, including the Flask app, the page template, and the Docker configuration, without AI. An AI coding agent later wrote a small security fix that escapes WHOIS responses before they're shown on the page, and upgraded the Python version, dependencies, and Docker configuration; the maintainer read and verified every line of those changes. The agent also added a check that rejects anything that isn't a valid domain name, which the maintainer reviewed but didn't verify line by line, so the project is rated Reviewed overall.

The agent has also helped with documentation, such as `CLAUDE.md` and `CHANGELOG.md`, which doesn't count toward the AI Share. Its changes are reviewed by a second AI before they're committed, which doesn't change the oversight level.
