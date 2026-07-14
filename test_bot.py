import pandas as pd
import requests

# Yeh hamara test data hai jisme English, Script Urdu, aur Roman Urdu teeno shamil hain
test_payloads = [
    {"message_id": "m1", "sender_id": "+923001112223", "text": "Hello, I want to start"},
    {"message_id": "m2", "sender_id": "+923001112223", "text": "مجھے ہیلپ چاہیے، کسی ایجنٹ سے بات کروائیں"},
    {"message_id": "m3", "sender_id": "+923001112224", "text": "shukriya aap ka bot acha hai"},
    {"message_id": "m4", "sender_id": "+923001112225", "text": "What are your timings?"}
]

api_url = "http://127.0.0.1:8000/whatsapp/webhook"
execution_results = []

print("--- Testing SafeX Solutions Multi-language Module ---")

for data in test_payloads:
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        res_json = response.json()
        execution_results.append({
            "User Input": data["text"],
            "Detected Lang": res_json["detected_language"],
            "Intent": res_json["resolved_intent"],
            "Bot Reply": res_json["reply_text"]
        })

# Pandas DataFrame banayein taake output bilkul saaf aur table format mein dikhe
df = pd.DataFrame(execution_results)
print(df.to_string(index=False))