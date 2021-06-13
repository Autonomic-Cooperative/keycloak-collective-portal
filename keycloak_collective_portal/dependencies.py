"""Route dependencies."""

from datetime import datetime as dt
from datetime import timedelta

from fastapi import Depends, Request
from humanize import naturaldelta


async def fresh_token(request: Request):
    """Ensure fresh credentials for speaking to Keycloak."""
    from keycloak_collective_portal.keycloak import init_keycloak

    request.app.state.keycloak = init_keycloak()


async def logged_in(request: Request):
    """Ensure the user is logged in."""
    from keycloak_collective_portal.exceptions import RequiresLoginException

    user = request.session.get("user")

    if not user:
        raise RequiresLoginException

    return user


async def get_user(request: Request):
    """Retrieve the user object."""
    return request.session.get("user")


async def get_invites(request: Request, user=Depends(get_user)):
    """Retrieve all invites from storage."""
    from keycloak_collective_portal.config import INVITE_TIME_LIMIT

    all_invites = {}

    for username in await request.app.state.redis.keys("*"):
        invites = await request.app.state.redis.get(username)

        for invite in invites:
            invite["validity"] = naturaldelta(
                dt.fromisoformat(invite["time"])
                + timedelta(days=INVITE_TIME_LIMIT)
            )

        all_invites[username] = invites

    return all_invites
