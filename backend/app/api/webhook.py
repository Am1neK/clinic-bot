import os
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from backend.app.prompts import detect_intent_and_lang, generate_faq_reply
from backend.app.utils import send_whatsapp_text

router = APIRouter()

# GET endpoint for Meta webhook verification
@router.get("/")
async def verify(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    return Response(status_code=403)

@router.post("/")
async def webhook(req: Request):
    body = await req.json()
    try:
        msg_obj = body["entry"][0]["changes"][0]["value"]["messages"][0]
        from_id = msg_obj["from"]
        text = msg_obj.get("text", {}).get("body", "")
    except Exception:
        return {"status": "ignored"}

    intent, lang = detect_intent_and_lang(text)

    if intent == "BOOK":
        send_whatsapp_text(from_id, "Okay, let’s book an appointment. What date works for you?")
    elif intent == "FAQ":
        clinic_facts = "Open Mon-Fri 9–6. Services: GP, blood tests."
        reply = generate_faq_reply(text, clinic_facts, lang)
        send_whatsapp_text(from_id, reply)
    else:
        send_whatsapp_text(from_id, "Sorry, I didn’t understand. Reply BOOK to schedule.")

    return {"status":"ok"}
