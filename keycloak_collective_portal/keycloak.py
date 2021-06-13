"""Keycloak logic."""

from keycloak import KeycloakAdmin


def init_keycloak():
    """Initialise Keycloak client."""
    from keycloak_collective_portal.config import (
        KEYCLOAK_CLIENT_SECRET,
        KEYCLOAK_DOMAIN,
        KEYCLOAK_REALM,
    )

    client = KeycloakAdmin(
        server_url=f"https://{KEYCLOAK_DOMAIN}/auth/",
        realm_name=KEYCLOAK_REALM,
        client_secret_key=KEYCLOAK_CLIENT_SECRET,
        verify=True,
    )

    return client
