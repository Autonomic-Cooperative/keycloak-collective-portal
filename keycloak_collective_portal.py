"""Community Keycloak SSO user management."""

from os import environ

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

APP_SECRET_KEY = environ.get("APP_SECRET_KEY")
KEYCLOAK_CLIENT_ID = environ.get("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = environ.get("KEYCLOAK_CLIENT_SECRET")
KEYCLOAK_DOMAIN = environ.get("KEYCLOAK_DOMAIN")
KEYCLOAK_REALM = environ.get("KEYCLOAK_REALM")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY)
templates = Jinja2Templates(directory="templates")

oauth = OAuth()
oauth.register(
    name="keycloak",
    client_kwargs={"scope": "openid profile email offline_access"},
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret=KEYCLOAK_CLIENT_SECRET,
    authorize_url=f"https://{KEYCLOAK_DOMAIN}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth",
    access_token_url=f"https://{KEYCLOAK_DOMAIN}/auth/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")
    if user:
        return templates.TemplateResponse(
            "index.html", context={"request": request, "user": user}
        )
    return RedirectResponse(request.url_for("login_keycloak"))


@app.get("/login/keycloak")
async def login_keycloak(request: Request):
    redirect_uri = request.url_for("auth_keycloak")
    return await oauth.keycloak.authorize_redirect(request, redirect_uri)


@app.get("/auth/keycloak")
async def auth_keycloak(request: Request):
    try:
        token = await oauth.keycloak.authorize_access_token(request)
        user = await oauth.keycloak.parse_id_token(request, token)
        request.session["user"] = dict(user)
        return RedirectResponse(request.url_for("home"))
    except Exception as exception:
        return HTMLResponse(f"<h1>{str(exception)}</h1>")


@app.route("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(request.url_for("home"))
