# keycloak-collective-portal

[![Build Status](https://drone.autonomic.zone/api/badges/autonomic-cooperative/keycloak-collective-portal/status.svg?ref=refs/heads/main)](https://drone.autonomic.zone/autonomic-cooperative/keycloak-collective-portal)

> Community Keycloak SSO user management

This is a tiny Python app that allows you create custom web pages, outside of
the Keycloak administration interface, which can be used to manage users in
Keycloak. This is done via the REST API. It was designed with collective
management in mind. Existing Keycloak users can authenticate with the app and
then do things like invite others, send verification emails and so on. Anything
that the REST API supports, this app can support. We aim to strive for the
maximum usability which is often lacking in Enterprise Software ™ environments.
This is the No Admins, No Masters edition of Keycloak.

## Getting Started

### From a system adminstrator perspective

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

### From a collective member perspective

- Visit `https://<your-portal-url>` (ask your system adminstrator friends)
- Log in with your usual login details
- Follow the instructions on the web page to perform administrative actions

## Hacking

It's a [FastAPI](https://fastapi.tiangolo.com/) application.

```
$ make
```
