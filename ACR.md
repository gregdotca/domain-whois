---
rating: B3b
spec: "0.1"
updated: 2026-10-11
---

# AI Code Rating

**ACR B3b** (Maintainer: Experienced · AI Share: 51–75% · Oversight: Reviewed)

This project is rated with [AI Code Rating](https://aicoderating.com/spec/0.1/), spec version 0.1.

## How AI Was Used

The maintainer wrote the original Domain WHOIS Lookup, including the Flask app, the page template, and the Docker configuration, without AI. An AI coding agent later wrote a small security fix that escapes WHOIS responses before they're shown on the page, and upgraded the Python version, dependencies, and Docker configuration; the maintainer read and verified every line of those changes. The agent also added a check that rejects anything that isn't a valid domain name, moved the Tailwind and daisyUI styles from a CDN to a build step in the Dockerfile, added automatic dark mode, fixed lookups of punycode domains, and wrote the project's tests, which together make up just over half of the code. The maintainer chose the approach and the themes, and reviewed these changes but didn't verify them line by line, so the project is rated Reviewed overall. The vendored daisyUI plugin and jQuery files aren't counted.

The agent has also helped with documentation, such as `CLAUDE.md` and `CHANGELOG.md`, which doesn't count toward the AI Share. Its changes are reviewed by a second AI before they're committed, which doesn't change the oversight level.
