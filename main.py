from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateProfileRequest
from datetime import datetime
import json
import os
import asyncio
from colorama import Fore, Style, init

# تهيئة الألوان
init(autoreset=True)

# إعدادات Telegram API
api_id = 22997958
api_hash = '60b28759c231d582aa4fc06042e5ad65'
phone_number = '0096407864864798'

# إنشاء عميل Telegram
client = TelegramClient('Raafat', api_id, api_hash)
SETTINGS_FILE = "settings.json"

# تحميل أو إنشاء ملف الإعدادات
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {"format": "12", "my_id": None}

settings.setdefault("my_id", None)

# حفظ الإعدادات
def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# إعادة تحميل الإعدادات
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"format": "12", "my_id": None}

# تحويل الوقت إلى أرقام جميلة
def beautify_time(time_string):
    mapping = {"0": "𝟎", "1": "𝟏", "2": "𝟐", "3": "𝟑", "4": "𝟒",
               "5": "𝟓", "6": "𝟔", "7": "𝟕", "8": "𝟖", "9": "𝟗"}
    return ''.join(mapping.get(char, char) for char in time_string)

# الحصول على الوقت بالتنسيق المختار
def get_time():
    current_settings = load_settings()
    return datetime.now().strftime('%I:%M' if current_settings["format"] == "12" else '%H:%M')

# الأوامر
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

# تغيير الاسم حسب الوقت
async def change_name():
    prev_time = ""
    while True:
        try:
            current_time = get_time()
            beautified_time = beautify_time(current_time)
            if current_time != prev_time:
                await client(UpdateProfileRequest(first_name=beautified_time))
                prev_time = current_time
            await asyncio.sleep(5)  # مدة التحديث (يمكن تعديلها)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

# تشغيل العميل
async def main():
    await client.start(phone_number)
    if settings["my_id"] is None:
        me = await client.get_me()
        settings["my_id"] = me.id
        save_settings()

# طباعة البنر وتشغيل المهام
with client:
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
 ██████╗ ███╗   ███╗ █████╗ ██████╗ ████████╗████████╗██╗███╗   ███╗███████╗
██╔═══██╗████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║████╗ ████║██╔════╝
██║   ██║██╔████╔██║███████║██████╔╝   ██║      ██║   ██║██╔████╔██║█████╗  
██║   ██║██║╚██╔╝██║██╔══██║██╔═══╝    ██║      ██║   ██║██║╚██╔╝██║██╔══╝  
╚██████╔╝██║ ╚═╝ ██║██║  ██║██║        ██║      ██║   ██║██║ ╚═╝ ██║███████╗
 ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝      ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝
"""
    print(banner)
    client.loop.run_until_complete(asyncio.gather(main(), change_name()))