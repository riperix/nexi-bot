import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💜 Добро пожаловать в NEXI CASE!\n\n"
        "Если ты оплатил покупку в Mini App, заявка придёт сюда."
    )


async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not OWNER_ID:
        await update.message.reply_text("❌ Бот ещё не настроен.")
        return

    message = (
        "💳 НОВАЯ ЗАЯВКА НА ПРОВЕРКУ ОПЛАТЫ\n\n"
        f"👤 Имя: {user.full_name}\n"
        f"🆔 Telegram ID: {user.id}\n"
        f"📱 Username: @{user.username or 'нет'}\n\n"
        "Пользователь сообщил, что оплатил покупку."
    )

    await context.bot.send_message(
        chat_id=int(OWNER_ID),
        text=message
    )

    await update.message.reply_text(
        "✅ Заявка отправлена администратору!\n"
        "После проверки тебе будут начислены коины 💜"
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("Не найден BOT_TOKEN")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("paid", paid))

    print("NEXI BOT запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
