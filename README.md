# SafeX Solutions - WhatsApp Auto-Reply Bot
## Multi-language Support Module (Week 2 Contribution)

This repository contains the dynamic language detection and routing module developed for the SafeX Solutions WhatsApp chatbot.

### Features
* **Automatic Language Detection:** Detects whether the user is typing in English or Urdu (Script).
* **Intent Mapping:** Maps incoming messages to key intents (`welcome`, `agent`, `thank_you`, `fallback`).
* **Automated Localized Replies:** Responds to the user in their preferred/detected language automatically.

### Files
* `main.py` - The core FastAPI backend server with NLP language routing.
* `test_bot.py` - Automation script to test English and Urdu response flows.
