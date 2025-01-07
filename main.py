
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


# إنشاء عميل Telegram
client = TelegramClient('Oliver', api_id, api_hash)
SETTINGS_FILE = "settings.json"

# تحميل أو إنشاء ملف الإعدادات
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
else:
    settings = {"style": "default", "format": "12", "my_id": None}

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
    return {"style": "default", "format": "12", "my_id": None}

# أنماط الزخرفة المختلفة
styles = {
    "default": lambda s: s,  # النمط الافتراضي بدون زخرفة
    "مزخرف1": lambda s: ''.join({"0": "𝟎", "1": "𝟏", "2": "𝟐", "3": "𝟑", "4": "𝟒",
                                 "5": "𝟓", "6": "𝟔", "7": "𝟕", "8": "𝟖", "9": "𝟗"}.get(char, char) for char in s),
    "عربي": lambda s: ''.join({"0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤",
                               "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"}.get(char, char) for char in s),
    "مزخرف2": lambda s: ''.join({"0": "⓪", "1": "①", "2": "②", "3": "③", "4": "④",
                                 "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨"}.get(char, char) for char in s)
}

# تطبيق الزخرفة حسب النمط الحالي
def apply_style(text):
    current_settings = load_settings()
    style = current_settings.get("style", "default")
    return styles.get(style, lambda x: x)(text)

# الحصول على الوقت بالتنسيق المختار
def get_time():
    current_settings = load_settings()
    return datetime.now().strftime('%I:%M' if current_settings["format"] == "12" else '%H:%M')

# الأوامر
@client.on(events.NewMessage(pattern=r'^\.start$'))
async def dot_start(event):
    if event.sender_id == settings["my_id"]:
        await event.respond(
            "<b>✨ أهلاً بك في سورس <u>𝗦𝗺𝗮𝗿𝘁𝗧𝗶𝗺𝗲</u>! 👋</b>\n"
            "<i>🛠️ الأوامر المتاحة:</i>\n\n"
            "<code>.الأنماط</code> - عرض الأنماط المتاحة لتزيين الوقت.\n"
            "<code>.تنسيق الوقت</code> - عرض أنظمة تنسيق الوقت (12/24 ساعة).\n\n"
            "<b>⌚ يتم تحديث الوقت تلقائيًا حسب الإعدادات.</b>\n\n"
            "<a href='https://t.me/oliceer'>🧑‍💻 المطور: 𝗢𝗹𝗶𝗰𝗲𝗲𝗿</a>",
            parse_mode="html"
        )

@client.on(events.NewMessage(pattern=r'^\.الأنماط$'))
async def dot_styles(event):
    if event.sender_id == settings["my_id"]:
        await event.respond(
            "<b>⌚ الأنماط المتاحة لتغيير شكل الساعة:</b>\n\n"
            "<code>.افتراضي</code> - لا يوجد زخرفة.\n"
            "<code>.مزخرف1</code> - نمط الزخرفة الأول.\n"
            "<code>.عربي</code> - الأرقام العربية.\n"
            "<code>.مزخرف2</code> - نمط الزخرفة الثاني.\n",
            parse_mode="html"
        )

@client.on(events.NewMessage(pattern=r'^\.تنسيق الوقت$'))
async def time_format_page(event):
    if event.sender_id == settings["my_id"]:
        await event.respond(
            "<b>⌚ أنظمة التنسيق المتاحة:</b>\n\n"
            "<code>.نظام12</code> - لتعيين تنسيق الوقت بنظام 12 ساعة.\n"
            "<code>.نظام24</code> - لتعيين تنسيق الوقت بنظام 24 ساعة.\n",
            parse_mode="html"
        )

# تغيير النمط
@client.on(events.NewMessage(pattern=r'^\.افتراضي$'))
async def set_default(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = "default"
        save_settings()
        await event.respond("<b>✅ تم اختيار النمط الافتراضي.</b>", parse_mode="html")

@client.on(events.NewMessage(pattern=r'^\.مزخرف1$'))
async def set_fancy1(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = "مزخرف1"
        save_settings()
        await event.respond("<b>✅ تم اختيار نمط الزخرفة الأول.</b>", parse_mode="html")

@client.on(events.NewMessage(pattern=r'^\.عربي$'))
async def set_arabic(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = "عربي"
        save_settings()
        await event.respond("<b>✅ تم اختيار نمط الأرقام العربية.</b>", parse_mode="html")

@client.on(events.NewMessage(pattern=r'^\.مزخرف2$'))
async def set_fancy2(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = "مزخرف2"
        save_settings()
        await event.respond("<b>✅ تم اختيار نمط الزخرفة الثاني.</b>", parse_mode="html")

# أوامر تغيير التنسيق
@client.on(events.NewMessage(pattern=r'^\.نظام12$'))
async def set_12(event):
    if event.sender_id == settings["my_id"]:
        settings["format"] = "12"
        save_settings()
        await event.respond("<b>✅ تم اختيار تنسيق الوقت بنظام 12 ساعة.</b>", parse_mode="html")

@client.on(events.NewMessage(pattern=r'^\.نظام24$'))
async def set_24(event):
    if event.sender_id == settings["my_id"]:
        settings["format"] = "24"
        save_settings()
        await event.respond("<b>✅ تم اختيار تنسيق الوقت بنظام 24 ساعة.</b>", parse_mode="html")

# تغيير الاسم حسب الوقت والنمط
async def change_name():
    prev_time = ""
    while True:
        try:
            current_time = get_time()
            beautified_time = apply_style(current_time)  # تطبيق الزخرفة
            if current_time != prev_time:
                await client(UpdateProfileRequest(first_name=beautified_time))
                prev_time = current_time
            await asyncio.sleep(5)  # مدة التحديث
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

