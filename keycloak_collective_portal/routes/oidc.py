"""OpenID Connect routes."""

import httpx
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from keycloak_collective_portal.dependencies import logged_in

router = APIRouter()


@router.get("/login")
async def login(request: Request):
    from keycloak_collective_portal.config import AUTOMATICALLY_LOG_IN

    if AUTOMATICALLY_LOG_IN:
        return RedirectResponse(request.url_for("login_keycloak"))

    return request.app.state.templates.TemplateResponse(
        "login.html", context={"request": request}
    )


@router.get("/login/keycloak")
async def login_keycloak(request: Request):
    redirect_uri = request.url_for("auth_keycloak")
    return await request.app.state.oidc.keycloak.authorize_redirect(
        request, redirect_uri
    )


@router.get("/auth/keycloak")
async def auth_keycloak(request: Request):
    try:
        token = await request.app.state.oidc.keycloak.authorize_access_token(
            request
        )
    except Exception as exc:
        return HTMLResponse(f"<p>{exc} (<a href='/'>home</a>)</p>")

    user = await request.app.state.oidc.keycloak.parse_id_token(request, token)
    request.session["user"] = dict(user)

    return RedirectResponse(request.url_for("home"))


@router.get("/logout", dependencies=[Depends(logged_in)])
async def logout(request: Request):
    from keycloak_collective_portal.config import KEYCLOAK_BASE_URL

    try:
        httpx.get(f"{KEYCLOAK_BASE_URL}/logout")
    except Exception as exc:
        return HTMLResponse(f"<p>{exc} (<a href='/'>home</a>)</p>")

    request.session.pop("user", None)

    return RedirectResponse(request.url_for("login"))
