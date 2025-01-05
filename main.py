from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import json
import os
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)
api_id = 22997958
api_hash = '60b28759c231d582aa4fc06042e5ad65'

client = TelegramClient('session_name', api_id, api_hash)
SETTINGS_FILE = "settings.json"

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {"format": "12", "my_id": None}

if "my_id" not in settings:
    settings["my_id"] = None

with open(SETTINGS_FILE, "w") as f:
    json.dump(settings, f)

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

def beautify_time(time_string):
    mapping = {"0": "𝟎", "1": "𝟏", "2": "𝟐", "3": "𝟑", "4": "𝟒",
               "5": "𝟓", "6": "𝟔", "7": "𝟕", "8": "𝟖", "9": "𝟗"}
    return ''.join(mapping.get(char, char) for char in time_string)

def get_time():
    if settings["format"] == "12":
        return datetime.now().strftime('%I:%M')
    else:
        return datetime.now().strftime('%H:%M')

@client.on(events.NewMessage(pattern=r'^\.start$'))
async def dot_start(event):
    if event.sender_id == settings["my_id"]:
        await event.respond(
            "<b>✨ أهلاً بيك بسورس <u>𝗦𝗺𝗮𝗿𝘁𝗧𝗶𝗺𝗲</u>! 👋</b>\n"
            "<i>🛠️ الأوامر المتاحة:</i>\n\n"
            "<code>🔹 set_12</code> - لتعيين تنسيق الوقت إلى 12 ساعة.\n"
            "<code>🔹 set_24</code> - لتعيين تنسيق الوقت إلى 24 ساعة.\n\n"
            "<b>⌚ يتم تحديث الوقت تلقائيًا حسب الإعدادات.</b>\n\n"
            "<a href='https://t.me/oliceer'>🧑‍💻 المطور: 𝗢𝗹𝗶𝗰𝗲𝗲𝗿</a>",
            parse_mode="html"
        )

@client.on(events.NewMessage(pattern='set_12'))
async def set_12(event):
    if event.sender_id == settings["my_id"]:
        settings["format"] = "12"
        save_settings()
        await event.respond("<b>✅ تم اختيار تنسيق الوقت بنظام 12 ساعة.</b>", parse_mode="html")

@client.on(events.NewMessage(pattern='set_24'))
async def set_24(event):
    if event.sender_id == settings["my_id"]:
        settings["format"] = "24"
        save_settings()
        await event.respond("<b>✅ تم اختيار تنسيق الوقت بنظام 24 ساعة.</b>", parse_mode="html")

async def change_name():
    prev_time = ""
    while True:
        try:
            current_time = get_time()
            beautified_time = beautify_time(current_time)
            if current_time != prev_time:
                await client(UpdateProfileRequest(first_name=beautified_time))
                prev_time = current_time
            await asyncio.sleep(1.5)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

async def main():
    # تحقق مما إذا كان هناك جلسة موجودة بالفعل
    if not await client.is_user_authorized():
        phone_number = input("Enter your phone number (with country code): ")  # Request phone number if not authorized
        await client.start(phone_number)
    else:
        print("You are already logged in!")
    
    if settings["my_id"] is None:
        me = await client.get_me()
        settings["my_id"] = me.id
        save_settings()

with client:
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
 ██████╗ ███╗   ███╗ █████╗ ██████╗ ████████╗████████╗██╗███╗   ███╗███████╗
██╔═══██╗████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║████╗ ████║██╔════╝
██║   ██║██╔████╔██║███████║██████╔╝   ██║      ██║   ██║██╔████╔██║█████╗  
██║   ██║██║╚██╔╝██║██╔══██║██╔═══╝    ██║      ██║   ██║██║╚██╔╝██║██╔══╝  
╚██████╔╝██║ ╚═╝ ██║██║  ██║██║        ██║      ██║   ██║██║ ╚═╝ ██║███████╗
 ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝      ╚══╝   ╚═╝╚═╝     ╚═╝╚══════╝
"""
    print(banner)
    client.loop.run_until_complete(asyncio.gather(main(), change_name()))