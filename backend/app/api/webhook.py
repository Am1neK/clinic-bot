from fastapi import APIRouter, Request, Response
from fastapi.responses import PlainTextResponse
import os

router = APIRouter()

@router.get("/")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)  # ✅ return challenge if token matches
    return Response(status_code=403)  # ❌ reject if wrong token

