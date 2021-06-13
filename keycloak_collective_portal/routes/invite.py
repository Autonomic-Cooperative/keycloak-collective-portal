"""Routes for invite logic."""

from datetime import datetime as dt
from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from keycloak_collective_portal.dependencies import (
    get_invites,
    get_user,
    logged_in,
)

router = APIRouter()


@router.get("/invite/keycloak/create", dependencies=[Depends(logged_in)])
async def invite_keycloak_create(
    request: Request, user=Depends(get_user), invites=Depends(get_invites)
):
    username = user["preferred_username"]

    new_invite = {"link": str(uuid4()), "time": str(dt.now())}
    request.app.state.log.info(f"Generated new invite: {new_invite}")

    invites = await request.app.state.redis.get(username)
    if invites:
        invites.append(new_invite)
    else:
        invites = [new_invite]

    await request.app.state.redis.set(username, invites)

    return RedirectResponse(request.url_for("home"))


@router.get("/invite/keycloak/delete", dependencies=[Depends(logged_in)])
async def invite_keycloak_delete(
    request: Request, user=Depends(get_user), invites=Depends(get_invites)
):
    username = user["preferred_username"]
    invite_to_delete = request.query_params.get("invite")

    invites = await request.app.state.redis.get(username)
    request.app.state.log.info(f"Retrieved invites: {invites}")

    purged = [i for i in invites if i["link"] != invite_to_delete]
    request.app.state.log.info(f"Purged invites: {invites}")

    await request.app.state.redis.set(user["preferred_username"], purged)

    return RedirectResponse(request.url_for("home"))
