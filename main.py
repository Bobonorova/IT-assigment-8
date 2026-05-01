import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# =====================
# CONFIG (BU YERNI O'ZGARTIRASIZ)
# =====================
TOKEN = "YOUR_BOT_TOKEN_HERE"
ALLOWED_USERS = [123456789]  # sizning Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# =====================
# CHECK USER
# =====================
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

# =====================
# FAMILY DATA (REAL EMAS - DEMO)
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

# =====================
# RANDOM PROFILE
# =====================
def profile(name):
    phone = f"+998 9{random.randint(0,9)} {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}"
    email = name.lower().replace(" ", "") + "@gmail.com"
    address = random.choice(cities)
    card = f"8600 **** **** {random.randint(1000,9999)}"

    return {
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
        "card": card
    }

# =====================
# KEYBOARDS
# =====================
def main_menu():
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
        types.InlineKeyboardButton("🔙 Back", callback_data="back"),
        types.InlineKeyboardButton("🏠 Home", callback_data="home")
    )
    return kb

# =====================
# START
# =====================
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not is_allowed(message.from_user.id):
        await message.answer("❌ Ruxsat yo‘q")
        return

    await message.answer(
        "🇺🇿 *Family Dashboard*\n\nA’zoni tanlang:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =====================
# PROFILE
# =====================
@dp.callback_query_handler(lambda c: c.data in family)
async def show(callback: types.CallbackQuery):
    if not is_allowed(callback.from_user.id):
        return

    data = profile(family[callback.data])

    text = f"""
👤 *{data['name']} profili*

📞 Telefon: {data['phone']}
📧 Email: {data['email']}
🏠 Manzil: {data['address']}
💳 Karta: {data['card']}
"""

    await callback.message.edit_text(
        text,
        reply_markup=nav(),
        parse_mode="Markdown"
    )

# =====================
# BACK
# =====================
@dp.callback_query_handler(lambda c: c.data == "back")
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🇺🇿 *Family Dashboard*\n\nA’zoni tanlang:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =====================
# HOME
# =====================
@dp.callback_query_handler(lambda c: c.data == "home")
async def home(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🇺🇿 *Family Dashboard*\n\nA’zoni tanlang:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

# =====================
# RUN
# =====================
if __name__ == "__main__":
    executor.start_polling(dp)
