"""Home routes."""

from fastapi import APIRouter, Depends, Request

from keycloak_collective_portal.dependencies import (
    get_invites,
    get_user,
    logged_in,
)

router = APIRouter()


@router.get("/", dependencies=[Depends(logged_in)])
async def home(
    request: Request, user=Depends(get_user), invites=Depends(get_invites)
):
    context = {"request": request, "user": user, "invites": invites}
    return request.app.state.templates.TemplateResponse(
        "admin.html", context=context
    )
