# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a vulnerability

Open a GitHub issue with the `security` label, or contact the maintainer
through the repository. Please do not publish exploit details in a public
issue before the maintainer has had a chance to respond.

We aim to acknowledge reports within 3 working days.

## Scope notes for this tool

appstudy only ever makes plain HTTP GET requests to URLs the user names, on
the same origin, with a page budget and a delay. It never sends cookies,
credentials, or POST data, and it never executes downloaded content. If you
find a case where it does otherwise, that is a bug — please report it.

**Do not use appstudy to study a site you do not have a legitimate reason to
study.** Respect `robots.txt`, rate limits, and the site owner's wishes; a
tool for learning from public work is not a licence to hammer someone's server.
