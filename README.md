# keycloak-collective-portal

> **WARNING**: this software is in a pre-alpha quality state and is an initial
> prototype. It is being developed within the context of
> [lumbung.space](https://lumbung.space/) and may have hard-coded values and
> configuration specifically for that environment. If the idea of this software
> sounds interesting to you, please let us know on the issue tracker!

[![Build Status](https://drone.autonomic.zone/api/badges/autonomic-cooperative/keycloak-collective-portal/status.svg?ref=refs/heads/main)](https://drone.autonomic.zone/autonomic-cooperative/keycloak-collective-portal)

> Community Keycloak SSO user management

This is a tiny Python app that allows you create custom web pages, outside of
the Keycloak administration interface, which can be used to manage users in
Keycloak. This is done via the REST API. It was designed with collective
management in mind. Existing Keycloak users can authenticate with the app and
then do things like invite others, send verification emails and so on. Anything
that the REST API supports, this app can support. We aim to strive for the
usability which is often lacking in Enterprise Software ™ environments
(Keycloak is made within the context of RedHat / IBM). This is the No Admins,
No Masters edition of Keycloak.

## Getting Started

### From a system administrator perspective

A note on permissions: we use the `admin-cli` client and a fine grained, secure
access configuration for making requests from this app to your Keycloak
instance. We aim to follow the Keycloak documentation and recommended practices
on security so that `keycloak-colective-portal` is a safe option to add into
your technology stack.

- Ensure that your `admin-cli` client under your Client settings has the following config:
  - **Settings tab**:
      - **Access Type**: `confidential`
      - **Service Accounts Enabled**: `ON`
  - **Scope tab**:
      - **Full scope allowed**: `OFF`
      - **Client roles**: Under `realm-management` add `manage-users` and `view-users`
  - **Service Account Roles tab**:
      - **Client roles**: Under `realm-management` add `manage-users` and `view-users`
- Deploy using [`coop-cloud/keycloak-colective-portal`](https://git.autonomic.zone/coop-cloud/keycloak-collective-portal)
  - See the example [.envrc](./.envrc) for the configuration available, more documentation will follow soon.

### From a collective member perspective

- Visit `https://<your-portal-url>` (ask your system adminstrator friends)
- Log in with your usual login details
- Follow the instructions on the web page to perform administrative actions

## Hacking

It's a [FastAPI](https://fastapi.tiangolo.com/) application (if you know
[Flask](https://flask.palletsprojects.com/en/2.0.x/) /
[Sanic](https://sanic.readthedocs.io/en/stable/) then it is more or less the
same thing). Currently being developed with Python 3.9. Once we move out of the
prototype stage, more version compatability will be offered.

```
$ docker run -p 6379:6379 -d redis:6-alpine
$ set -a && source .envrc && set +a
$ make
```
