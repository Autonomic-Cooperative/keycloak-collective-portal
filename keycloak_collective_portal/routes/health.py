"""Healthcheck routes."""

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/healthz")
async def healthz(request: Request):
    return {"detail": "ALL ENGINES FIRING"}
