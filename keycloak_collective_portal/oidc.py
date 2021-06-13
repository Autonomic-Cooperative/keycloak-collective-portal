"""OpenID Connect logic."""

from authlib.integrations.starlette_client import OAuth, OAuthError


def init_oidc():
    """Initialise OIDC client."""
    from keycloak_collective_portal.config import (
        KEYCLOAK_BASE_URL,
        KEYCLOAK_CLIENT_ID,
        KEYCLOAK_CLIENT_SECRET,
        KEYCLOAK_SCOPES,
    )

    oidc = OAuth()
    oidc.register(
        name="keycloak",
        client_kwargs={"scope": KEYCLOAK_SCOPES},
        client_id=KEYCLOAK_CLIENT_ID,
        client_secret=KEYCLOAK_CLIENT_SECRET,
        authorize_url=f"{KEYCLOAK_BASE_URL}/auth",
        access_token_url=f"{KEYCLOAK_BASE_URL}/token",
        jwks_uri=f"{KEYCLOAK_BASE_URL}/certs",
    )
    return oidc
