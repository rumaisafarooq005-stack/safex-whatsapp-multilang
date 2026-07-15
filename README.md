# SafeX Solutions - Smart WhatsApp Auto-Reply Bot
## Dynamic Multi-language Support & Chat Assistant (Week 2 Integration)

An intelligent, multi-language (English/Urdu Script/Roman Urdu) conversational bot developed for SafeX Solutions. This project features a robust FastAPI backend combined with a modern, dark-mode ChatGPT-style web chatting interface.

---

## 🚀 Key Features

* **Intelligent Language Detection:** Automatically identifies whether the user is typing in English or Urdu script using NLP (`langdetect`).
* **Smart Roman Urdu Routing:** If the user types Urdu using English alphabets (e.g., *"baat karo"*, *"shukriya"*, *"kese ho"*), the bot automatically detects it and switches the response language to Urdu.
* **Expanded Intent Mapping:** Handles standard flows like `welcome`, `agent`, and `thank_you`, along with custom queries like company `services`, `pricing`, `about`, and `location`.
* **Lightweight ChatGPT-style Web UI:** A beautiful, responsive, dark-mode chatting interface (`index.html`) that allows users to interact with the FastAPI backend in real-time.
* **Interactive Chatty/Funny Mode:** Responds to informal prompts, tells programmer jokes, and identifies its developer!

---

## 📂 Project Structure

* `main.py` - The enhanced FastAPI backend with CORS enabled and intelligent language/intent routing.
* `index.html` - The frontend web client designed to look and feel exactly like ChatGPT.
* `test_bot.py` - Script used to test backend terminal execution.
* `README.md` - Technical documentation of the repository.

---

## 🛠️ How to Run Locally

1.  **Start the Backend Server:**
    Run the following command in your terminal/PowerShell inside the project directory:
    ```bash
    uvicorn main:app --reload
    ```
2.  **Open the Web Assistant:**
    Simply double-click and open `index.html` in any web browser to start chatting with the SafeX AI Assistant!
