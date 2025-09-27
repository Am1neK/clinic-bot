import os
import requests

WABA_PHONE_NUMBER_ID = os.getenv("WABA_PHONE_NUMBER_ID")
WABA_ACCESS_TOKEN = os.getenv("WABA_ACCESS_TOKEN")
GRAPH_API_URL = f"https://graph.facebook.com/v17.0/{WABA_PHONE_NUMBER_ID}/messages"

def send_whatsapp_text(to_whatsapp_id, text):
    headers = {"Authorization": f"Bearer {WABA_ACCESS_TOKEN}", "Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to_whatsapp_id,
        "type": "text",
        "text": {"body": text}
    }
    r = requests.post(GRAPH_API_URL, headers=headers, json=payload)
    return r.json()
