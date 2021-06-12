"""Community Keycloak SSO user management."""

import json
from datetime import datetime as dt
from datetime import timedelta
from os import environ
from uuid import uuid4

import httpx
from aioredis import create_redis_pool
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from humanize import naturaldelta
from starlette.exceptions import HTTPException
from starlette.middleware.sessions import SessionMiddleware

APP_SECRET_KEY = environ.get("APP_SECRET_KEY")

KEYCLOAK_CLIENT_ID = environ.get("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = environ.get("KEYCLOAK_CLIENT_SECRET")

KEYCLOAK_DOMAIN = environ.get("KEYCLOAK_DOMAIN")
KEYCLOAK_REALM = environ.get("KEYCLOAK_REALM")
BASE_URL = f"https://{KEYCLOAK_DOMAIN}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect"  # noqa

REDIS_DB = environ.get("REDIS_DB")
REDIS_HOST = environ.get("REDIS_HOST")
REDIS_PORT = environ.get("REDIS_PORT")

INVITE_TIME_LIMIT = environ.get("INVITE_TIME_LIMIT")

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY)
templates = Jinja2Templates(directory="templates")

oauth = OAuth()
oauth.register(
    name="keycloak",
    client_kwargs={"scope": "openid profile email"},
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret=KEYCLOAK_CLIENT_SECRET,
    authorize_url=f"{BASE_URL}/auth",
    access_token_url=f"{BASE_URL}/token",
    jwks_uri=f"{BASE_URL}/certs",
)


class RequiresLoginException(Exception):
    pass


@app.exception_handler(RequiresLoginException)
async def requires_login(request, exception):
    return RedirectResponse(request.url_for("login"))


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    home = request.url_for("login")
    return HTMLResponse(f"<p>{exc.detail} (<a href='{home}'>home</a>)</p>")


async def logged_in(request: Request):
    user = request.session.get("user")
    if not user:
        raise RequiresLoginException
    return user


async def get_user(request: Request):
    return request.session.get("user")


async def get_invites(request: Request, user=Depends(get_user)):
    username = user["preferred_username"]
    invites = await app.state.redis.get(username)
    if invites:
        humanised = []
        for invite in json.loads(invites):
            invite["human_time"] = naturaldelta(
                dt.fromisoformat(invite["time"])
                + timedelta(days=int(INVITE_TIME_LIMIT))
            )
            humanised.append(invite)
        return humanised
    return []


@app.on_event("startup")
async def starup_event():
    app.state.redis = await create_redis_pool(
        f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"
    )


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()


@app.get("/", dependencies=[Depends(logged_in)])
async def home(
    request: Request, user=Depends(get_user), invites=Depends(get_invites)
):
    context = {"request": request, "user": user, "invites": invites}
    return templates.TemplateResponse("admin.html", context=context)


@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse(
        "login.html", context={"request": request}
    )


@app.get("/login/keycloak")
async def login_keycloak(request: Request):
    redirect_uri = request.url_for("auth_keycloak")
    return await oauth.keycloak.authorize_redirect(request, redirect_uri)


@app.get("/auth/keycloak")
async def auth_keycloak(request: Request):
    try:
        token = await oauth.keycloak.authorize_access_token(request)
    except Exception as exc:
        return HTMLResponse(f"<p>{exc} (<a href='{home}'>home</a>)</p>")

    user = await oauth.keycloak.parse_id_token(request, token)
    request.session["user"] = dict(user)

    return RedirectResponse(request.url_for("home"))


@app.get("/logout", dependencies=[Depends(logged_in)])
async def logout(request: Request):
    try:
        httpx.get(f"{BASE_URL}/logout")
    except Exception as exc:
        return HTMLResponse(f"<p>{exc} (<a href='{home}'>home</a>)</p>")

    request.session.pop("user", None)

    return RedirectResponse(request.url_for("login"))


@app.get("/invite/keycloak/create", dependencies=[Depends(logged_in)])
async def invite_keycloak_create(
    request: Request, user=Depends(get_user), invites=Depends(get_invites)
):
    invites.append({"link": str(uuid4()), "time": str(dt.now())})
    app.state.redis.set(user["preferred_username"], json.dumps(invites))
    return RedirectResponse(request.url_for("home"))


@app.get("/invite/keycloak/delete", dependencies=[Depends(logged_in)])
async def invite_keycloak_delete(
    request: Request, user=Depends(get_user), invites=Depends(get_invites)
):
    invite =request.query_params.get("invite")
    # TODO
