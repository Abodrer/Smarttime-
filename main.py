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

# تطبيق الزخرفة حسب النمط الحالي
def apply_style(text, style):
    return style(text)

# الحصول على الوقت بالتنسيق المختار
def get_time():
    current_settings = load_settings()
    return datetime.now().strftime('%I:%M' if current_settings["format"] == "12" else '%H:%M')

# الوظائف الخاصة بالأنماط:
def default_style(s):
    return s

# تأكد من أن الأنماط هي دوال أو دوال قابلة للتطبيق، لا سلاسل نصية
styles = {
    "default": lambda s: s,  # النمط الافتراضي بدون زخرفة
    
    "مزخرف1": lambda s: ''.join({"0": "𝟎", "1": "𝟏", "2": "𝟐", "3": "𝟑", "4": "𝟒",
                                 "5": "𝟓", "6": "𝟖", "7": "𝟖", "8": "𝟖", "9": "𝟗"}.get(char, char) for char in s),
    
    "عربي": lambda s: ''.join({"0": "٠", "1": "١", "2": "٢", "3": "٣", "4": "٤",
                               "5": "٥", "6": "٦", "7": "٧", "8": "٨", "9": "٩"}.get(char, char) for char in s),
    
    "مزخرف2": lambda s: ''.join({"0": "⓪", "1": "①", "2": "②", "3": "③", "4": "④",
                                 "5": "⑤", "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨"}.get(char, char) for char in s),
    
    "مزخرف3": lambda s: ''.join({"0": "𝟬", "1": "𝟭", "2": "𝟮", "3": "𝟯", "4": "𝟰",
                                 "5": "𝟱", "6": "𝟲", "7": "𝟳", "8": "𝟴", "9": "𝟵"}.get(char, char) for char in s),
    
    "دوائر": lambda s: ''.join({"0": "⓿", "1": "➊", "2": "➋", "3": "➌", "4": "➍",
                                "5": "➎", "6": "➏", "7": "➐", "8": "➑", "9": "➒"}.get(char, char) for char in s),
    
    "خط تحت": lambda s: ''.join({"0": "0̲", "1": "1̲", "2": "2̲", "3": "3̲", "4": "4̲",
                                 "5": "5̲", "6": "6̲", "7": "7̲", "8": "8̲", "9": "9̲"}.get(char, char) for char in s),
    
    "خط فوق": lambda s: ''.join({"0": "0̅", "1": "1̅", "2": "2̅", "3": "3̅", "4": "4̅",
                                 "5": "5̅", "6": "6̅", "7": "7̅", "8": "8̅", "9": "9̅"}.get(char, char) for char in s),
    
    "قوسين": lambda s: ''.join({"0": "(0)", "1": "(1)", "2": "(2)", "3": "(3)", "4": "(4)",
                                "5": "(5)", "6": "(6)", "7": "(7)", "8": "(8)", "9": "(9)"}.get(char, char) for char in s),
    
    "رياضيات": lambda s: ''.join({"0": "⊖", "1": "⊗", "2": "⊙", "3": "⊚", "4": "⊛",
                                  "5": "⊝", "6": "⊞", "7": "⊟", "8": "⊠", "9": "⊡"}.get(char, char) for char in s),
    
    "قلوب": lambda s: ''.join({"0": "❤️", "1": "💙", "2": "💚", "3": "💛", "4": "💜",
                               "5": "💔", "6": "💖", "7": "💗", "8": "💘", "9": "💝"}.get(char, char) for char in s),
    
    "مربعات": lambda s: ''.join({"0": "🟥", "1": "🟩", "2": "🟦", "3": "🟧", "4": "🟨",
                                "5": "🟪", "6": "🟩", "7": "🟫", "8": "🟦", "9": "🟩"}.get(char, char) for char in s),
    
    "أسهم": lambda s: ''.join({"0": "⇨", "1": "⇦", "2": "⇧", "3": "⇩", "4": "⇗",
                               "5": "⇘", "6": "⇙", "7": "⇕", "8": "⇘", "9": "⇖"}.get(char, char) for char in s),
    
    "جوكر": lambda s: ''.join({"0": "⧫", "1": "♦", "2": "♣", "3": "♠", "4": "♥",
                               "5": "♦", "6": "♠", "7": "♣", "8": "♦", "9": "♥"}.get(char, char) for char in s),
}

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
            "<code>.مزخرف2</code> - نمط الزخرفة الثاني.\n"
            "<code>.مزخرف3</code> - نمط الزخرفة الثالث.\n"
            "<code>.دوائر</code> - الأرقام بدوائر.\n"
            "<code>.خط تحت</code> - الأرقام مع خط تحت.\n"
            "<code>.خط فوق</code> - الأرقام مع خط فوق.\n"
            "<code>.قوسين</code> - الأرقام داخل قوسين.\n"
            "<code>.رياضيات</code> - الأرقام بصيغة رياضية.\n"
            "<code>.قلوب</code> - الأرقام باستخدام القلوب.\n"
            "<code>.مربعات</code> - الأرقام داخل مربعات.\n"
            "<code>.أسهم</code> - الأرقام باستخدام الأسهم.\n"
            "<code>.جوكر</code> - الأرقام باستخدام رموز جوكر.\n",
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

# تغيير النمط# تغيير النمط
@client.on(events.NewMessage(pattern=r'^\.افتراضي$'))
async def set_default(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = default_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار النمط الافتراضي.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.مزخرف1$'))
async def set_fancy1(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = fancy_style1
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الزخرفة الأول.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.عربي$'))
async def set_arabic(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = arabic_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الأرقام العربية.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.مزخرف2$'))
async def set_fancy2(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = fancy_style2
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الزخرفة الثاني.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.مزخرف3$'))
async def set_fancy3(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = fancy_style3
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الزخرفة الثالث.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.دوائر$'))
async def set_circles(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = circles_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الدوائر.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.خط تحت$'))
async def set_underline(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = underline_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الخط تحت.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.خط فوق$'))
async def set_overline(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = overline_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الخط فوق.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.قوسين$'))
async def set_parentheses(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = parentheses_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الأقواس.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.رياضيات$'))
async def set_math(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = math_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الرياضيات.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.قلوب$'))
async def set_hearts(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = heart_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط القلوب.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.مربعات$'))
async def set_squares(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = square_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط المربعات.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.أسهم$'))
async def set_arrows(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = arrows_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الأسهم.</b>", parse_mode="html")
        await delete_after(event, msg)

@client.on(events.NewMessage(pattern=r'^\.جوكر$'))
async def set_joker(event):
    if event.sender_id == settings["my_id"]:
        settings["style"] = joker_style
        save_settings()
        msg = await event.respond("<b>✅ تم اختيار نمط الجوكر.</b>", parse_mode="html")
        await delete_after(event, msg)

# تغيير الاسم حسب الوقت والنمط
async def change_name():
    prev_time = ""
    while True:
        try:
            current_time = get_time()
            beautified_time = apply_style(current_time, settings.get("style", default_style))  # تطبيق الزخرفة
            if current_time != prev_time:
                await client(UpdateProfileRequest(first_name=beautified_time))
                prev_time = current_time
            await asyncio.sleep(5)  # مدة التحديث
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

# تشغيل العميل
async def main():
    await client.start()
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
   