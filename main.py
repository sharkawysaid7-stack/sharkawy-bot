import urllib.request
import urllib.parse
import json
import time
import os

# لو انت على Pydroid حطهم هنا، ولو على سيرفر هنحطهم هناك
TOKEN = os.environ.get("TOKEN", "9220079270:AAF3SeWz-HYfmGhhne9oZhru2vUl3OSxNCo")
GEMINI_KEY = os.environ.get("GEMINI_KEY", "AQ.Ab8RN6LJ1nYLNZTiiGMjbfamLBsraBnJ6M3owUAMz7YySizlnw")

BASE = f"https://api.telegram.org/bot{TOKEN}"
# ده الموديل الصح اللي شغال دلوقتي
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"

def send(chat_id, text):
    for i in range(0, len(text), 4000):
        part = text[i:i+4000]
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": part}).encode()
        try:
            urllib.request.urlopen(BASE + "/sendMessage", data)
        except:
            pass

def ask_gemini(question):
    prompt = f"""انت مساعد منصة شرقاوي لتعليم البرمجة.
جاوب بالعامية المصرية البسيطة.
اشرح ببساطة وادي مثال كود صغير.
السؤال: {question}"""
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    req = urllib.request.Request(GEMINI_URL, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("خطأ Gemini:", e)
        return "معلش حصل مشكلة، ابعت سؤالك تاني."

print("البوت شغال...")
offset = 0
while True:
    try:
        url = BASE + f"/getUpdates?offset={offset}&timeout=10"
        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read())
        for u in data.get("result", []):
            offset = u["update_id"] + 1
            msg = u.get("message")
            if msg:
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                print("وصلي:", text)
                if text == "/start":
                    send(chat_id, "أهلاً بيك في منصة شرقاوي 🤖\nابعت أي سؤال وأنا هجاوبك.")
                else:
                    send(chat_id, "ثانية واحدة بفكر... 🤔")
                    send(chat_id, ask_gemini(text))
    except Exception as e:
        print("خطأ:", e)
        time.sleep(2)
