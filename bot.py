import json
from datetime import datetime, time, timedelta
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    ChatJoinRequestHandler,
)

# ----------------- CONFIG -----------------
BOT_TOKEN = "8256240814:AAHggvBYHF-uTvnv-JB23tkV9nqwHLHbM3E"
CHANNEL_ID = -1001524647918  # private channel ID
TIMEZONE = "Asia/Dhaka"
USERS_FILE = "users.json"
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

# ----------------- Handlers -----------------
async def join_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat_id = update.chat_join_request.chat.id

    # ----------------- Fake / bot filter -----------------
    # Example: account must be older than 1 day (UTC)
    # Telegram API does not give join date, so advanced check skipped

    # ✅ Auto approve join request
    try:
        await context.bot.approve_chat_join_request(chat_id, user.id)
    except Exception as e:
        print(f"Could not approve join request for {user.id}: {e}")

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

    # schedule weekly jobs
    schedule_weekly_jobs(app)

    print("🤖 Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
