from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from database import save_order, get_orders
import os

# TOKEN (Railway Variables dan olinadi)
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

# USER DATA
user_data = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    await update.message.reply_text("📱 Xush kelibsiz!", reply_markup=keyboard)

# ADMIN BUYURTMALAR KO‘RISH
async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id != ADMIN_ID:
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

    # TELEFONLAR
    if text == "📱 Telefonlar":
        await update.message.reply_text("Telefon tanlang:", reply_markup=ReplyKeyboardMarkup(phones_menu, resize_keyboard=True))

    # IPHONE
    elif text == "🍎 iPhone 14":
        user_data[user_id] = {"phone": "iPhone 14"}

        await update.message.reply_text(
            "🍎 iPhone 14\n💰 1000$",
            reply_markup=ReplyKeyboardMarkup(buy_menu, resize_keyboard=True)
        )

    # SAMSUNG
    elif text == "🤖 Samsung S23":
        user_data[user_id] = {"phone": "Samsung S23"}

        await update.message.reply_text(
            "🤖 Samsung S23\n💰 900$",
            reply_markup=ReplyKeyboardMarkup(buy_menu, resize_keyboard=True)
        )

    # XIAOMI
    elif text == "📱 Xiaomi 13":
        user_data[user_id] = {"phone": "Xiaomi 13"}

        await update.message.reply_text(
            "📱 Xiaomi 13\n💰 700$",
            reply_markup=ReplyKeyboardMarkup(buy_menu, resize_keyboard=True)
        )

    # SOTIB OLISH
    elif text == "🛒 Sotib olish":
        if user_id not in user_data:
            user_data[user_id] = {}

        await update.message.reply_text("Ismingizni kiriting:")
        user_data[user_id]["step"] = "name"

    # NAME
    elif user_id in user_data and user_data[user_id].get("step") == "name":
        user_data[user_id]["name"] = text
        user_data[user_id]["step"] = "phone"
        await update.message.reply_text("Telefon raqamingizni kiriting:")

    # PHONE
    elif user_id in user_data and user_data[user_id].get("step") == "phone":
        user_data[user_id]["number"] = text
        order = user_data[user_id]

        save_order(order["name"], order["number"], order["phone"])

        msg = (
            f"🆕 YANGI BUYURTMA!\n\n"
            f"📱 Telefon: {order['phone']}\n"
            f"👤 Ism: {order['name']}\n"
            f"📞 Raqam: {order['number']}"
        )

        await update.message.reply_text("✅ Buyurtma qabul qilindi!")
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

        user_data[user_id] = {}

    # ORQAGA
    elif text == "🔙 Orqaga":
        await update.message.reply_text("Asosiy menyu", reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True))

    elif text == "ℹ️ Biz haqimizda":
        await update.message.reply_text("Biz ishonchli telefon do‘konimiz 📱")

    elif text == "📞 Aloqa":
        await update.message.reply_text("+998901234567")

# MAIN
def main():
    if not TOKEN:
        print("❌ TOKEN topilmadi! Railway Variables tekshiring!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("orders", orders))
    app.add_handler(MessageHandler(filters.TEXT, message_handler))

    print("🚀 Bot ishlayapti...")
    app.run_polling()

if __name__ == "__main__":
    main()
