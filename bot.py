from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from database import save_order, get_orders
import os

# TOKEN
TOKEN = os.getenv("TOKEN")

# ADMIN ID
ADMIN_ID = 8095916235

# MENYULAR
main_menu = [
    ["📱 Telefonlar"],
    ["ℹ️ Biz haqimizda", "📞 Aloqa"]
]

phones_menu = [
    ["🍎 iPhone 14"],
    ["🤖 Samsung S23"],
    ["📱 Xiaomi 13"],
    ["🔙 Orqaga"]
]

buy_menu = [
    ["🛒 Sotib olish"],
    ["🔙 Orqaga"]
]

# USER STATE
user_data = {}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text("📱 Xush kelibsiz!", reply_markup=keyboard)


# ORDERS (ADMIN)
async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Ruxsat yo‘q")
        return

    orders = get_orders()

    if not orders:
        await update.message.reply_text("📭 Buyurtmalar yo‘q")
        return

    text = "📦 BUYURTMALAR:\n\n"

    for o in orders:
        text += f"#{o[0]} | {o[1]} | {o[2]} | {o[3]}\n"

    await update.message.reply_text(text)


# MESSAGE HANDLER
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # INIT USER STATE
    if user_id not in user_data:
        user_data[user_id] = {}

    state = user_data[user_id]

    # MENU: TELEFONLAR
    if text == "📱 Telefonlar":
        await update.message.reply_text(
            "Telefon tanlang:",
            reply_markup=ReplyKeyboardMarkup(phones_menu, resize_keyboard=True)
        )

    elif text == "🍎 iPhone 14":
        state.clear()
        state["phone"] = "iPhone 14"

        await update.message.reply_text(
            "🍎 iPhone 14\n💰 1000$",
            reply_markup=ReplyKeyboardMarkup(buy_menu, resize_keyboard=True)
        )

    elif text == "🤖 Samsung S23":
        state.clear()
        state["phone"] = "Samsung S23"

        await update.message.reply_text(
            "🤖 Samsung S23\n💰 900$",
            reply_markup=ReplyKeyboardMarkup(buy_menu, resize_keyboard=True)
        )

    elif text == "📱 Xiaomi 13":
        state.clear()
        state["phone"] = "Xiaomi 13"

        await update.message.reply_text(
            "📱 Xiaomi 13\n💰 700$",
            reply_markup=ReplyKeyboardMarkup(buy_menu, resize_keyboard=True)
        )

    # BUY ORDER START
    elif text == "🛒 Sotib olish":
        if "phone" not in state:
            await update.message.reply_text("Avval telefon tanlang ☝️")
            return

        state["step"] = "name"
        await update.message.reply_text("Ismingizni kiriting:")

    # NAME STEP
    elif state.get("step") == "name":
        state["name"] = text
        state["step"] = "phone_number"
        await update.message.reply_text("Telefon raqamingizni kiriting:")

    # PHONE STEP
    elif state.get("step") == "phone_number":
        state["number"] = text

        save_order(state["name"], state["number"], state["phone"])

        msg = (
            f"🆕 YANGI BUYURTMA!\n\n"
            f"📱 Telefon: {state['phone']}\n"
            f"👤 Ism: {state['name']}\n"
            f"📞 Raqam: {state['number']}"
        )

        await update.message.reply_text("✅ Buyurtma qabul qilindi!")
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

        user_data[user_id] = {}

    # BACK
    elif text == "🔙 Orqaga":
        await update.message.reply_text(
            "Asosiy menyu",
            reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
        )

    elif text == "ℹ️ Biz haqimizda":
        await update.message.reply_text("Biz ishonchli telefon do‘konimiz 📱")

    elif text == "📞 Aloqa":
        await update.message.reply_text("+998901234567")


# MAIN
def main():
    if not TOKEN:
        print("❌ TOKEN topilmadi!")
        return

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .read_timeout(30)
        .write_timeout(30)
        .connect_timeout(30)
        .pool_timeout(30)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("orders", orders))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("🚀 Bot ishlayapti...")

    # IMPORTANT FIX
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
