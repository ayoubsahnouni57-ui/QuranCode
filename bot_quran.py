import asyncio
import datetime
import pytz
import os
from telegram import Bot

# Configuration
TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "-5393193827"

# Timezone Maroc
MAROC_TZ = pytz.timezone("Africa/Casablanca")

# Programme des cours
COURS = [
    (6, 30, 7, 30,   "تأملات وعبر في قصة قارون",           "ذ. سميرة"),
    (7, 45, 9,  0,   "تدبر ثمن من سورة آل عمران",           "ذ. عائشة"),
    (9,  0, 10, 30,  "سورة المائدة",                         "ذ. أسية"),
    (10, 30, 11, 30, "مواصلة تصحيح سورة آل عمران",          "ذ. رجاء"),
    (11, 30, 12, 45, "المفصل",                               "ذ. سميرة"),
    (14, 30, 15, 30, "مواصلة تصحيح سورة آل عمران",          "ذ. الحوصي"),
    (15, 30, 17,  0, "حصة الفقه",                           "ذ. يوسفي"),
    (17, 30, 18, 30, "سورة النساء",                          "ذ. أسية"),
    (18, 30, 19, 30, "حصة التجويد",                          "ذ. البردعي"),
    (19, 30, 20, 30, "موعظة",                                "ذ. نعيمة"),
    (21, 30, 22, 30, "تثبيت سورة البقرة",                   "ذ. بنفارس"),
]

def format_message(hd, md, hf, mf, matiere, prof):
    debut = f"{hd:02d}:{md:02d}"
    fin   = f"{hf:02d}:{mf:02d}"
    return (
        f"🌺 تذكير بالحصة القادمة 🌺\n\n"
        f"📚 *{matiere}*\n"
        f"👩‍🏫 {prof}\n"
        f"⏰ من {debut} إلى {fin}\n\n"
        f"_تبدأ الحصة خلال 10 دقائق_ 🕐"
    )

async def check_reminders(bot):
    while True:
        now = datetime.datetime.now(MAROC_TZ)
        print(f"⏰ Heure Maroc: {now.strftime('%H:%M:%S')}")
        for (hd, md, hf, mf, matiere, prof) in COURS:
            rappel_h = hd
            rappel_m = md - 10
            if rappel_m < 0:
                rappel_m += 60
                rappel_h -= 1

            if now.hour == rappel_h and now.minute == rappel_m and now.second < 30:
                msg = format_message(hd, md, hf, mf, matiere, prof)
                await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode="Markdown")
                print(f"✅ Message envoyé: {matiere}")
                await asyncio.sleep(60)

        await asyncio.sleep(20)

async def main():
    bot = Bot(token=TOKEN)
    print("🤖 Bot démarré - En attente des rappels...")
    await check_reminders(bot)

if __name__ == "__main__":
    asyncio.run(main())
