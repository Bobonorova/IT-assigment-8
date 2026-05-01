import os
import random
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# =====================
# CONFIG
# =====================
TOKEN = "YOUR_BOT_TOKEN_HERE"
ALLOWED_USERS = [123456789]

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"https://YOUR-RENDER-URL.onrender.com{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

app = Flask(__name__)

# =====================
# CHECK USER
# =====================
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

# =====================
# FAMILY DATA
# =====================
family = {
    "dad": "Azizbek Karimov",
    "mom": "Malika Karimova",
    "me": "Siz",
    "bro": "Javlonbek Karimov",
    "sis": "Nilufar Karimova"
}

cities = [
    "Toshkent, Yunusobod",
    "Samarqand, Registon",
    "Andijon, Shahrixon",
    "Farg‘ona, Marg‘ilon",
    "Buxoro, G‘ijduvon"
]

def gen(name):
    phone = f"+998 9{random.randint(0,9)} {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}"
    email = name.lower().replace(" ", "") + "@gmail.com"
    address = random.choice(cities)
    card = f"8600 **** **** {random.randint(1000,9999)}"

    return phone, email, address, card

# =====================
# KEYBOARD
# =====================
def menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("👨 Dadam", callback_data="dad"),
        types.InlineKeyboardButton("👩 Onam", callback_data="mom"),
        types.InlineKeyboardButton("🙋 Men", callback_data="me"),
        types.InlineKeyboardButton("👦 Akam", callback_data="bro"),
        types.InlineKeyboardButton("👶 Ukam", callback_data="sis"),
    )
    return kb

def nav():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("🏠 Menu", callback_data="home")
    )
    return kb

# =====================
# START MESSAGE
# =====================
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not is_allowed(message.from_user.id):
        return await message.answer("❌ Ruxsat yo‘q")

    await message.answer(
        "🇺🇿 *Family Web Bot*\n\nA’zoni tanlang:",
        reply_markup=menu(),
        parse_mode="Markdown"
    )

# =====================
# CALLBACK HANDLER
# =====================
@dp.callback_query_handler(lambda c: c.data in family)
async def show(callback: types.CallbackQuery):
    if not is_allowed(callback.from_user.id):
        return

    name = family[callback.data]
    phone, email, address, card = gen(name)

    text = f"""
👤 *{name} profili*

📞 Telefon: {phone}
📧 Email: {email}
🏠 Manzil: {address}
💳 Karta: {card}
"""

    await callback.message.edit_text(text, reply_markup=nav(), parse_mode="Markdown")

# =====================
# HOME
# =====================
@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🇺🇿 *Family Web Bot*\n\nA’zoni tanlang:",
        reply_markup=menu(),
        parse_mode="Markdown"
    )

# =====================
# WEBHOOK ROUTE
# =====================
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update = types.Update(**request.json)
    dp.process_update(update)
    return "ok"

# =====================
# START SERVER
# =====================
if __name__ == "__main__":
    from aiogram.utils.executor import start_webhook

    async def on_startup(dp):
        await bot.set_webhook(WEBHOOK_URL)

    async def on_shutdown(dp):
        await bot.delete_webhook()

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
