import logging
from fastapi import FastAPI
from pydantic import BaseModel
from langdetect import detect, DetectorFactory

# DetectorFactory ko seed dena zaroori hai taake har dafa accurate result mile
DetectorFactory.seed = 0

app = FastAPI(title="SafeX Solutions - Multi-language Engine")

# Terminal par logs dekhne ke liye configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MultiLangBot")

# 1. Responses Matrix (English aur Urdu dono ke jawabat)
RESPONSES = {
    "en": {
        "welcome": "Hello! Welcome to SafeX Solutions. How can we assist you today?",
        "fallback": "I'm sorry, I didn't quite catch that. Could you please rephrase?",
        "agent": "Connecting you to a live support agent. Please hold on.",
        "thank_you": "Thank you for contacting SafeX Solutions!"
    },
    "ur": {
        "welcome": "السلام علیکم! SafeX Solutions میں خوش آمدید۔ آج ہم آپ کی کیا مدد کر سکتے ہیں؟",
        "fallback": "معذرت، میں آپ کی بات سمجھ نہیں پایا۔ کیا آپ آسان الفاظ میں دوبارہ لکھ سکتے ہیں؟",
        "agent": "آپ کو لائیو سپورٹ ایجنٹ سے جوڑا جا رہا ہے۔ براہ کرم انتظار فرمائیں۔",
        "thank_you": "SafeX Solutions سے رابطہ کرنے کا بہت شکریہ!"
    }
}

# 2. Intent Keywords (User ke alfaz se maqsad pehchanna)
# Isme humne Roman Urdu aur Script Urdu dono ke liye basic support rakhi hai
INTENT_KEYWORDS = {
    "welcome": {
        "en": ["hello", "hi", "hey", "start"],
        "ur": ["ہیلو", "سلام", "السلام", "shuru", "aslam"]
    },
    "agent": {
        "en": ["agent", "human", "help", "support", "call"],
        "ur": ["ایجنٹ", "نمائندہ", "madad", "help", "agent", "rabta"]
    },
    "thank_you": {
        "en": ["thanks", "thank you", "bye"],
        "ur": ["شکریہ", "shukriya", "allah hafiz", "خدا حافظ"]
    }
}

# 3. Request and Response Data Models
class WhatsAppMessage(BaseModel):
    message_id: str
    sender_id: str
    text: str

class BotResponse(BaseModel):
    detected_language: str
    resolved_intent: str
    reply_text: str

# 4. Helper Functions
def identify_language(text: str) -> str:
    """User ke text ki language maloom karne ka function"""
    if not text.strip():
        return "en"
    try:
        lang = detect(text)
        # Agar language Urdu, Persian, ya Arabic script mein ho to 'ur' set karein
        if lang in ["ur", "fa", "ar"]:
            return "ur"
        return "en"
    except Exception:
        # Agar detection fail ho jaye to safe side par English select hogi
        return "en"

def extract_intent(text: str, lang: str) -> str:
    """Yeh function check karta hai ke user chahta kya hai"""
    clean_text = text.lower().strip()
    
    for intent, languages in INTENT_KEYWORDS.items():
        keywords = languages.get(lang, [])
        if any(keyword in clean_text for keyword in keywords):
            return intent
            
    # Agar text Roman Urdu mein hai par language detect 'en' hui, to urdu keywords bhi check kar lete hain
    if lang == "en":
        for intent, languages in INTENT_KEYWORDS.items():
            if any(kw in clean_text for kw in languages.get("ur", [])):
                return intent

    return "fallback"

# 5. API Endpoint (Yeh API apke baqi Group Members ke kaam aayegi)
@app.post("/whatsapp/webhook", response_model=BotResponse)
async def process_whatsapp_message(payload: WhatsAppMessage):
    user_input = payload.text
    
    # Step A: Language Detect karein
    detected_lang = identify_language(user_input)
    logger.info(f"Incoming message from {payload.sender_id}. Detected Language: {detected_lang}")
    
    # Step B: Intent nikaalein
    intent = extract_intent(user_input, detected_lang)
    
    # Step C: Language aur Intent ke mutabiq sahi jawab chunein
    final_reply = RESPONSES.get(detected_lang, RESPONSES["en"]).get(intent, RESPONSES["en"]["fallback"])
    
    return BotResponse(
        detected_language=detected_lang,
        resolved_intent=intent,
        reply_text=final_reply
    )