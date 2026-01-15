import json
from datetime import datetime, time, timedelta
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatJoinRequestHandler,
    CommandHandler,
)

# ----------------- CONFIG -----------------
BOT_TOKEN = "8256240814:AAHggvBYHF-uTvnv-JB23tkV9nqwHLHbM3E"
CHANNEL_ID = -1001524647918  # private channel ID
TIMEZONE = "Asia/Dhaka"
USERS_FILE = "users.json"
OWNER_ID = 5894250379
TEMPLATES_FILE = "templates.json"
# ------------------------------------------

# Welcome DM message
WELCOME_TEXT = """👋 Hi You Know!

📊 CB TRADERS BD 📊
Traders with big losses are now recovering fast and achieving their daily profit targets after joining our VIP group 💰

👉 Message me – @cb1traderbd ✅

🔥 Join us | Recover fast | Earn daily 🔥
"""

# Weekly channel post
WEEKLY_CHANNEL_MSG = """🌿আপনি এখনো কি ভাবতেছেন? CB TRADERS BD এর ডেইলি লাইভ সিগনালের রিভিও এবং ফ্রিতে দেওয়া ফিউচার সিগনালের একুরেসি দেখে আপনি খুশি নন? 🤔

🥀যদি আপনারও মনে হয় যে এরকম ডেইলি প্রফিট করতে তাহলে এখনি নিচে দেওয়া লিংক থেকে একাউন্ট খুলে এডমিনকে মেসেন দেন।🥰

🔗 Worldwide: https://broker-qx.pro/sign-up/?lid=1270194
🔗 For BD: https://market-qx.pro/sign-up/?lid=1270194
"""

# Weekly DM broadcast
WEEKLY_DM_MSG = """🥳 Hey Dear,

আপনি কি এখনো CB ELITE গ্রুপে জয়েন করেন নাই? 🤔 আজকে শুক্রবার এই ছুটির দিন উপলক্ষে আপনার জন্য মাত্র ১০$ ডিপজিটে জয়েন করানো হবে CB ELITE, CB FUTURE SIGNAL, CB ALL PAID SOFTWARE গ্রুপে তাই দেরি না করে নিচে দেওয়া বাটনে ক্লিক করে জয়েন করুন। 🥰
"""

# ----------------- Helper Functions -----------------
def save_user(user_id: int):
    try:
        with open(USERS_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []  # empty file বা invalid JSON থাকলে নতুন list
    except FileNotFoundError:
        data = []

    if user_id not in data:
        data.append(user_id)
        with open(USERS_FILE, "w") as f:
            json.dump(data, f)

# -------- Message Template Helpers --------
def load_templates():
    try:
        with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_templates(data):
    with open(TEMPLATES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ----------------- Handlers -----------------
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = update.chat_join_request.chat.id

    # Auto approve join request
    try:
        await context.bot.approve_chat_join_request(chat_id, user.id)
    except Exception as e:
        print(f"Could not approve join request: {e}")

    # Save user for DM broadcast
    save_user(user.id)

    # DM welcome message with Contact Admin button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/cb1traderbd?text=I%20want%20to%20Join%20CB%20VIP")]
    ])

    try:
        await context.bot.send_message(
            chat_id=user.id,
            text=WELCOME_TEXT,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Could not send DM to {user.id}: {e}")

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Save user to users.json
    save_user(user_id)

    start_text = """📢 আমাদের VIP সিগনাল গ্রুপে যুক্ত হতে হলে প্রথমেই একটি Quotex অ্যাকাউন্ট খুলতে হবে।
🔹 নিচের লিংকে ক্লিক করে আপনার একাউন্ট তৈরি করুন 👇
👉 https://broker-qx.pro/sign-up/?lid=1581667

🎬 ধাপে ধাপে গাইডলাইন
1️⃣ কিভাবে একাউন্ট খুলবেন:
👉 যদি একাউন্ট খুলতে না পারেন, তাহলে এই ভিডিওটি দেখুন 👇
🎥 https://youtu.be/7Yhi-Txmy9U?si=rfVTLqL2wm7gzRNa

2️⃣ ট্রেডিং কি ও কিভাবে কাজ করে:
🎥 বিস্তারিত জানতে এই ভিডিওটি দেখুন 👇
📘 https://youtu.be/RI3qSu208a8?si=GYv87W7VvFCQjj_Z

3️⃣ একাউন্ট খোলা সম্পন্ন হলে Deposit করুন:
🎥 Deposit করার নিয়ম জানতে এই ভিডিওটি দেখুন 👇
💳 https://youtu.be/9mGAqrgSqY4?si=BZ_Z0sj3_z7MFoZV

⚠️ গুরুত্বপূর্ণ তথ্য:
🔸 শুধুমাত্র যারা আমাদের লিংক দিয়ে একাউন্ট খুলবেন, তারাই আমাদের VIP সিগনাল ও সাপোর্ট পাবেন।
🔸 যদি আগে থেকে Quotex অ্যাকাউন্ট থাকে, তাহলে পুরনো অ্যাকাউন্ট ডিলিট করে নতুন Gmail দিয়ে আমাদের লিংক থেকে নতুন একাউন্ট খুলুন।

– [CB TRADERS BD]
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎁 Free Signal", url="https://t.me/+R_kEsY9yqkA1NDI1"),
            InlineKeyboardButton("📞 Contact Admin", url="https://t.me/cb1traderbd?text=I%20want%20to%20Join%20CB%20VIP")
        ]
    ])

    image_url = "https://i.postimg.cc/htm6fbMp/IMG-20260110-193941-832.jpg"

    try:
        await context.bot.send_photo(
            chat_id=user_id,
            photo=image_url,
            caption=start_text,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Could not send start message to {user_id}: {e}")

async def send_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id != OWNER_ID:
        await update.message.reply_text("❌ You are not allowed to use this command.")
        return

    text = update.message.text or ""
    lines = text.split("\n")

    if len(lines) < 4:
        await update.message.reply_text(
            "❌ Format:\n"
            "/message <channel_id> <photo_url_or_file_id_or_none>\n"
            "<message or caption>\n"
            "<button name>\n"
            "<button link>"
        )
        return

    try:
        # Parse channel_id and optional photo
        parts = lines[0].split(maxsplit=2)
        channel_id = int(parts[1])
        photo_input = parts[2] if len(parts) > 2 else None

        button_name = lines[-2].strip()
        button_link = lines[-1].strip()
        message_text = "\n".join(lines[1:-2]).strip()

        # Replace templates if any
        templates = load_templates()
        for key, value in templates.items():
            message_text = message_text.replace(f"{{{{{key}}}}}", value)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(button_name, url=button_link)]
        ])

        # Send photo if photo_input exists, else send text
        if photo_input and photo_input.lower() != "none":
            await context.bot.send_photo(
                chat_id=channel_id,
                photo=photo_input,
                caption=message_text,
                reply_markup=keyboard
            )
        else:
            await context.bot.send_message(
                chat_id=channel_id,
                text=message_text,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )

        await update.message.reply_text("✅ Sent successfully!")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def save_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    text = update.message.text or ""
    lines = text.split("\n")

    if len(lines) < 2 or len(lines[0].split()) < 2:
        await update.message.reply_text(
            "❌ Usage:\n/save <template_name>\n<template content>"
        )
        return

    name = lines[0].split(maxsplit=1)[1].strip()
    content = "\n".join(lines[1:]).strip()

    if not content:
        await update.message.reply_text("❌ Template content empty.")
        return

    # Save template
    data = load_templates()
    data[name] = content
    save_templates(data)

    await update.message.reply_text(f"✅ Template '{name}' saved!")

    # Save user for DM broadcast
    save_user(update.effective_user.id)

    # DM welcome message with Contact Admin button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "📞 Contact Admin",
            url="https://t.me/cb1traderbd?text=I%20want%20to%20Join%20CB%20VIP"
        )]
    ])

    # ✅ Safe DM inside async function
    try:
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=WELCOME_TEXT,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Could not send DM to {update.effective_user.id}: {e}")

# Weekly channel post
async def weekly_channel_post(context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📞 Contact Admin", url="https://t.me/cb1traderbd?text=I%20want%20to%20Join%20CB%20VIP")]
    ])
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=WEEKLY_CHANNEL_MSG, reply_markup=keyboard)
    except Exception as e:
        print(f"Could not send channel post: {e}")

# Weekly DM broadcast
async def weekly_dm(context: ContextTypes.DEFAULT_TYPE):
    try:
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    for user_id in users:
        try:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("Join Now", url="https://t.me/cb1traderbd?text=I%20want%20to%20Join%20CB%20VIP")]
            ])
            await context.bot.send_message(chat_id=user_id, text=WEEKLY_DM_MSG, reply_markup=keyboard)
        except Exception as e:
            print(f"Could not send DM to {user_id}: {e}")
            continue

# ----------------- Scheduler -----------------
def schedule_weekly_jobs(app):
    tz = pytz.timezone(TIMEZONE)

    # Next Friday 9 PM
    now = datetime.now(tz)
    days_ahead = 4 - now.weekday()  # Friday = 4
    if days_ahead < 0:
        days_ahead += 7
    next_friday = datetime.combine(now.date() + timedelta(days=days_ahead), time(hour=21, minute=0), tzinfo=tz)

    delta = (next_friday - now).total_seconds()

    # schedule channel post
    app.job_queue.run_repeating(weekly_channel_post, interval=7*24*60*60, first=delta)
    # schedule DM broadcast
    app.job_queue.run_repeating(weekly_dm, interval=7*24*60*60, first=delta)

# ----------------- Main -----------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(join_request))
    app.add_handler(CommandHandler("message", send_message_command))
    app.add_handler(CommandHandler("save", save_template))
    app.add_handler(CommandHandler("start", start_handler))

    # schedule weekly jobs
    schedule_weekly_jobs(app)

    print("🤖 Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()