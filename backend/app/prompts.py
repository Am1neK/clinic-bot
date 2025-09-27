import os
import openai
from langdetect import detect

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

SYSTEM_PROMPT = """You are ClinicAssist, a polite bilingual assistant. 
You do NOT diagnose. 
Always suggest booking an appointment. 
Reply in the user’s language (English, Malay, Mandarin)."""

def detect_intent_and_lang(user_message):
    try:
        lang = detect(user_message)
        if lang.startswith("ms"):
            lang = "ms"
        elif lang.startswith("zh"):
            lang = "zh"
        else:
            lang = "en"
    except:
        lang = "en"

    prompt = f"Classify into: BOOK, CANCEL, FAQ, OTHER. Reply only label. Message: {user_message}"
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role":"system","content":"Classifier"},
                  {"role":"user","content":prompt}],
        max_tokens=10,
        temperature=0
    )
    label = resp["choices"][0]["message"]["content"].strip()
    return label, lang

def generate_faq_reply(user_message, clinic_facts, lang="en"):
    resp = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role":"system","content":SYSTEM_PROMPT},
                  {"role":"user","content":f"{user_message}. Clinic facts: {clinic_facts}"}],
        max_tokens=150,
        temperature=0.3
    )
    return resp["choices"][0]["message"]["content"].strip()
