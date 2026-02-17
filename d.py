import asyncio
from telethon import TelegramClient, events
import re
import aiohttp

API_ID = 36272084
API_HASH = "6d6b4ed35d626f945da79945514b35f8"

WEBHOOK_URL = "https://otp-buy.shop/webhook_otp.php"
SECRET_TOKEN = "otp_7xK92_secure"

# 👉 Add all accounts here (sessions already created locally)
accounts = [
    { "phone": "+19713024409", "session": "session1" },
    { "phone": "+16518423797", "session": "session2" },
    { "phone": "+919202205014", "session": "session3" },
    { "phone": "+19132940367", "session": "session4" },
    { "phone": "+19042274632", "session": "session5" },
]

otp_regex = r"\b\d{4,6}\b"
clients = []

async def setup_client(phone, session_name, http_session):
    client = TelegramClient(session_name, API_ID, API_HASH)

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        message = event.raw_text
        match = re.search(otp_regex, message)
        if match:
            otp = match.group(0)
            print(f"[+] OTP Detected ({phone}): {otp}")
            try:
                async with http_session.post(
                    WEBHOOK_URL,
                    data={"token": SECRET_TOKEN, "phone": phone, "otp": otp},
                    timeout=10
                ) as resp:
                    text = await resp.text()
                    print("[+] Webhook Response:", text)
            except Exception as e:
                print("[-] Error sending OTP:", e)

    # अब OTP नहीं माँगेगा क्योंकि session files पहले से मौजूद हैं
    await client.start()
    print(f"[*] Listening for OTP messages on {phone}...")
    clients.append(client)

async def main():
    async with aiohttp.ClientSession() as http_session:
        # सभी clients parallel start होंगे
        await asyncio.gather(*(setup_client(acc["phone"], acc["session"], http_session) for acc in accounts))
        # सभी clients disconnect होने तक alive रहेंगे
        await asyncio.gather(*(client.run_until_disconnected() for client in clients))

asyncio.run(main())
