from telethon import TelegramClient, events
import re
import requests
import asyncio

API_ID = 36272084
API_HASH = "6d6b4ed35d626f945da79945514b35f8"

PHONE_NUMBER = "+19713024409"  # only for sending to webhook
session_name = "session1"

webhook_url = "https://2tg.daamanclub.store/webhook_otp.php"
secret_token = "otp_7xK92_secure"

client = TelegramClient(session_name, API_ID, API_HASH)

otp_regex = r"\b\d{4,6}\b"

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    message = event.raw_text
    match = re.search(otp_regex, message)

    if match:
        otp = match.group(0)
        print(f"[+] OTP Detected: {otp}")

        try:
            r = requests.post(webhook_url, data={
                "token": secret_token,
                "phone": PHONE_NUMBER,
                "otp": otp
            }, timeout=10)

            print("[+] Webhook Response:", r.text)
        except Exception as e:
            print("[-] Error:", e)

async def main():
    # ❗ IMPORTANT: No phone login in cloud
    await client.start()
    print("[*] Listening for OTP messages...")
    await client.run_until_disconnected()

asyncio.run(main())
