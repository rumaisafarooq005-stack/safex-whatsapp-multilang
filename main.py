import logging
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

app = FastAPI(title="SafeX Solutions - Ultimate Support Bot")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MultiLangBot")

# 1. Broad and Funny Responses Matrix
RESPONSES = {
    "en": {
        "welcome": "Hello! Welcome to SafeX Solutions. How can we assist you today?",
        "fallback": "I understand you are speaking English, but I didn't quite catch that. Try asking about our 'services', 'pricing', or even ask me to tell a 'joke'!",
        "agent": "Connecting you to a live support agent. Please hold on.",
        "thank_you": "You are very welcome! Thank you for contacting SafeX Solutions.",
        # SafeX Custom Queries
        "services": "SafeX Solutions offers cutting-edge AI WhatsApp bots, Web Development, Cloud Security, and Custom ERP Systems!",
        "pricing": "Our pricing depends on your requirements! But don't worry, we offer very pocket-friendly packages starting from $49/month for small businesses.",
        "about": "SafeX Solutions is a leading software company dedicated to automating businesses using artificial intelligence and smart technologies.",
        "location": "We are located in Pakistan, but we serve clients globally! You can also connect with us online.",
        # Funny/Chatty Baatein
        "funny": "Why do programmers wear glasses? Because they can't C#! 😂",
        "creator": "I was created by Rumaisa, the star software engineer of SafeX Solutions! She is my boss. 😎",
        "how_are_you": "I'm an AI, so I don't sleep, I don't eat, but I'm 100% charged and ready to help you!"
    },
    "ur": {
        "welcome": "السلام علیکم! SafeX Solutions میں خوش آمدید۔ آج ہم آپ کی کیا مدد کر سکتے ہیں؟",
        "fallback": "میں آپ کی بات سمجھنے کی کوشش کر رہا ہوں۔ آپ ہماری 'خدمات' (services)، 'قیمت' (pricing) کے بارے میں پوچھ سکتے ہیں، یا مجھے کوئی 'لطیفہ' (joke) سنانے کو کہہ سکتے ہیں!",
        "agent": "آپ کو لائیو سپورٹ ایجنٹ سے جوڑا جا رہا ہے۔ براہ کرم انتظار فرمائیں۔",
        "thank_you": "رابطہ کرنے کا بہت بہت شکریہ! اگر مزید کوئی کام ہو تو ضرور بتائیں۔",
        # SafeX Custom Queries
        "services": "سیف ایکس سلوشنز (SafeX) آپ کو آرٹیفیشل انٹیلیجنس واٹس ایپ بوٹس، ویب ڈویلپمنٹ، کلاؤڈ سیکیورٹی اور سافٹ ویئر سلوشنز فراہم کرتا ہے۔",
        "pricing": "ہماری قیمتیں آپ کی ضروریات کے مطابق ہوتی ہیں! چھوٹے کاروباروں کے لیے ہمارے پیکجز صرف 12,000 روپے ماہانہ سے شروع ہوتے ہیں۔",
        "about": "سیف ایکس سلوشنز ایک جدید سافٹ ویئر کمپنی ہے جو کاروباری اداروں کو اے آئی (AI) اور سمارٹ ٹیکنالوجی کے ذریعے خودکار (automate) بنانے میں مدد کرتی ہے۔",
        "location": "ہمارا ہیڈ آفس پاکستان میں ہے، لیکن ہم پوری دنیا میں اپنے کلائنٹس کو خدمات فراہم کرتے ہیں۔",
        # Funny/Chatty Baatein
        "funny": "ایک پروگرامر نے دوسرے سے پوچھا: زندگی کیسی گزر رہی ہے؟ دوسرے نے جواب دیا: بس 'Errors' دور کرتے کرتے خود 'Error' بن گیا ہوں! 😜",
        "creator": "مجھے رومیسہ (Rumaisa) نے بنایا ہے، جو سیف ایکس سلوشنز کی سب سے ذہین سافٹ ویئر ڈویلپر ہیں! 😎",
        "how_are_you": "میں بالکل فٹ فاٹ ہوں! نہ مجھے بھوک لگتی ہے نہ پیاس، بس چوبیس گھنٹے آپ کی خدمت کے لیے تیار رہتا ہوں۔"
    }
}

# 2. Expanded Keywords to match Urdu/English & Funny stuff
INTENT_KEYWORDS = {
    "welcome": {
        "en": ["hello", "hi", "hey", "start", "greetings", "helo"],
        "ur": ["ہیلو", "سلام", "السلام", "shuru", "aslam", "salam"]
    },
    "agent": {
        "en": ["agent", "human", "help", "support", "call", "talk to someone", "live chat"],
        "ur": ["ایجنٹ", "نمائندہ", "madad", "help", "rabta", "baat", "human", "numainda"]
    },
    "thank_you": {
        "en": ["thanks", "thank you", "bye", "okay", "ok", "great"],
        "ur": ["شکریہ", "shukriya", "allah hafiz", "خدا حافظ", "shukria", "theek hai"]
    },
    # SafeX Queries
    "services": {
        "en": ["services", "what do you do", "products", "features", "work", "portfolio"],
        "ur": ["کام", "سروس", "خدمات", "kya karte ho", "services", "kaam", "projects"]
    },
    "pricing": {
        "en": ["pricing", "price", "cost", "how much", "charges", "packages", "cheap"],
        "ur": ["قیمت", "پیسے", "charges", "package", "paise", "price", "qemat"]
    },
    "about": {
        "en": ["about", "company", "safex", "who are you", "what is safex"],
        "ur": ["کمپنی", "سیف ایکس", "safex kya hai", "safex kon hai", "maloomat"]
    },
    "location": {
        "en": ["location", "office", "address", "where", "city"],
        "ur": ["دفتر", "پتہ", "kahan", "office", "address", "location"]
    },
    # Funny & Personal Questions
    "funny": {
        "en": ["joke", "funny", "laugh", "make me laugh", "tell me a joke"],
        "ur": ["لطیفہ", "lateefa", "joke", "hanso", "funny", "koi mazaq"]
    },
    "creator": {
        "en": ["creator", "who made you", "boss", "owner", "developer", "built"],
        "ur": ["کس نے بنایا", "kisne banaya", "creator", "boss", "rumaisa", "developer"]
    },
    "how_are_you": {
        "en": ["how are you", "how r u", "how is it going", "are you okay"],
        "ur": ["کیسے ہو", "کیا حال ہے", "kese ho", "kia hal hai", "thik ho"]
    }
}

# Roman Urdu indicators list
ROMAN_URDU_INDICATORS = [
    "urdu", "baat karo", "bolo", "karo", "kya", "hal", "kaise", "ho", "tum", 
    "meri", "suno", "hai", "nhi", "nahi", "shukriya", "shukria", "kisne", 
    "banaya", "kahan", "office", "lateefa", "kese", "hal", "helo", "kaam"
]

class WhatsAppMessage(BaseModel):
    message_id: str
    sender_id: str
    text: str

class BotResponse(BaseModel):
    detected_language: str
    resolved_intent: str
    reply_text: str

def identify_language(text: str) -> str:
    clean_text = text.lower().strip()
    if not clean_text:
        return "en"
    
    # Check 1: Script check
    try:
        lang = detect(clean_text)
        if lang in ["ur", "fa", "ar"]:
            return "ur"
    except Exception:
        pass
    
    # Check 2: Roman Urdu keywords check
    words = clean_text.split()
    for word in words:
        if word in ROMAN_URDU_INDICATORS:
            return "ur"
            
    return "en"

def extract_intent(text: str, lang: str) -> str:
    clean_text = text.lower().strip()
    
    # Primary check for exact language match
    for intent, languages in INTENT_KEYWORDS.items():
        keywords = languages.get(lang, [])
        if any(keyword in clean_text for keyword in keywords):
            return intent
            
    # Secondary cross-check
    for intent, languages in INTENT_KEYWORDS.items():
        all_keywords = languages.get("en", []) + languages.get("ur", [])
        if any(kw in clean_text for kw in all_keywords):
            return intent

    return "fallback"

@app.post("/whatsapp/webhook", response_model=BotResponse)
async def process_whatsapp_message(payload: WhatsAppMessage):
    user_input = payload.text
    
    detected_lang = identify_language(user_input)
    logger.info(f"Text: '{user_input}' -> Detected Language: {detected_lang}")
    
    intent = extract_intent(user_input, detected_lang)
    logger.info(f"Resolved Intent: {intent}")
    
    # Chose response
    if intent == "funny":
        final_reply = RESPONSES[detected_lang]["funny"]
    else:
        final_reply = RESPONSES.get(detected_lang, RESPONSES["en"]).get(intent, RESPONSES["en"]["fallback"])
    
    return BotResponse(
        detected_language=detected_lang,
        resolved_intent=intent,
        reply_text=final_reply
    )