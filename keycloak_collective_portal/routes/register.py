"""Registration routes."""

import json
from datetime import datetime as dt
from datetime import timedelta

from fastapi import APIRouter, Depends, Form, Request

from keycloak_collective_portal.dependencies import get_invites

router = APIRouter()


@router.get("/register/{invite}")
async def register_invite(
    request: Request, invite: str, invites=Depends(get_invites)
):
    from keycloak_collective_portal.config import INVITE_TIME_LIMIT

    matching, username, matching_invite = False, None, None
    for username in invites:
        for _invite in invites[username]:
            if invite == _invite["link"]:
                matching = True
                username = username
                matching_invite = _invite

    if not matching:
        message = "This invite does not exist, sorry."
        context = {"request": request, "message": message}
        return request.app.state.templates.TemplateResponse(
            "invalid.html", context=context
        )

    expired = (
        dt.fromisoformat(matching_invite["time"])
        + timedelta(days=INVITE_TIME_LIMIT)
    ).day > dt.now().day

    if expired:
        message = "This invite has expired, sorry."
        context = {"request": request, "message": message}
        return request.app.state.templates.TemplateResponse(
            "invalid.html", context=context
        )

    context = {"request": request, "username": username}
    return request.app.state.templates.TemplateResponse(
        "register.html", context=context
    )


@router.post("/form/keycloak/register")
def form_keycloak_register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    payload = {
        "email": email,
        "username": username,
        "enabled": True,
        "firstName": first_name,
        "lastName": last_name,
        "credentials": [
            {
                "value": password,
                "type": "password",
            }
        ],
        "realmRoles": [
            "user_default",
        ],
    }

    try:
        user_id = request.app.state.keycloak.create_user(
            payload, exist_ok=False
        )
        request.app.state.keycloak.send_verify_email(user_id=user_id)
    except Exception as exception:
        message = json.loads(exception.error_message).get(
            "errorMessage", "Unknown reason!"
        )
        context = {"request": request, "exception": message}
        return request.app.state.templates.TemplateResponse(
            "submit.html", context=context
        )

    context = {"request": request, "email": email}
    return request.app.state.templates.TemplateResponse(
        "submit.html", context=context
    )
