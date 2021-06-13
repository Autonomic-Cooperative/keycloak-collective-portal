"""App entrypoint."""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException
from starlette.middleware.sessions import SessionMiddleware

from keycloak_collective_portal.config import (
    APP_SECRET_KEY,
    APP_THEME,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
    STATIC_DIR,
    TEMPLATE_DIR,
)
from keycloak_collective_portal.exceptions import RequiresLoginException
from keycloak_collective_portal.keycloak import init_keycloak
from keycloak_collective_portal.oidc import init_oidc
from keycloak_collective_portal.redis import Redis
from keycloak_collective_portal.routes import (
    health,
    invite,
    oidc,
    register,
    root,
)

app = FastAPI(docs_url=None, redoc_url=None)


@app.exception_handler(RequiresLoginException)
async def requires_login(request, exception):
    return RedirectResponse(request.url_for("login"))


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    home = request.url_for("login")
    return HTMLResponse(f"<p>{exc.detail} (<a href='{home}'>home</a>)</p>")


@app.on_event("startup")
async def starup_event():
    redis = Redis()
    app.state.redis = await redis.create_pool(
        f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"
    )


@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()


app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.state.oidc = init_oidc()
app.state.keycloak = init_keycloak()
app.state.templates = Jinja2Templates(directory=TEMPLATE_DIR)
app.state.theme = APP_THEME

app.include_router(invite.router)
app.include_router(oidc.router)
app.include_router(register.router)
app.include_router(root.router)
app.include_router(health.router)
