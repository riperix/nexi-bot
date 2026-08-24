import os
import json

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ТВОЙ TELEGRAM ID
OWNER_ID = 1282434336

# ССЫЛКА НА ТВОЁ MINI APP
WEB_APP_URL = "https://riperix.github.io/nexi-mini-app/"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            KeyboardButton(
                text="💜 ОТКРЫТЬ NEXI CASES",
                web_app=WebAppInfo(url=WEB_APP_URL),
            )
        ]
    ]

    await update.message.reply_text(
        "💜 Добро пожаловать в NEXI CASES!\n\n"
        "Нажми кнопку ниже, чтобы открыть приложение.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
        ),
    )


async def web_app_payment(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    try:
        user = update.effective_user

        if not update.message.web_app_data:
            return

        data = json.loads(
            update.message.web_app_data.data
        )

        if data.get("type") != "payment_request":
            return

        coins = data.get("coins", "Не указано")
        price = data.get("price", "Не указано")

        username = (
            f"@{user.username}"
            if user.username
            else "нет username"
        )

        message = (
            "💳 НОВАЯ ЗАЯВКА НА ПРОВЕРКУ ОПЛАТЫ\n\n"
            f"👤 Имя: {user.full_name}\n"
            f"📱 Username: {username}\n"
            f"🆔 Telegram ID: {user.id}\n\n"
            f"💎 Пакет: {coins} NEXI COINS\n"
            f"💰 Сумма: {price} ₽\n\n"
            "⚠️ Пользователь нажал «Я ОПЛАТИЛ(А)»."
        )

        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=message,
        )

        print(
            f"Заявка успешно отправлена: "
            f"{user.id}, {coins} coins, {price} rub"
        )

    except Exception as error:
        print(f"ОШИБКА ЗАЯВКИ: {error}")


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    print(f"ОШИБКА БОТА: {context.error}")


def main():
    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN не найден в Railway Variables"
        )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30)
        .read_timeout(30)
        .write_timeout(30)
        .get_updates_read_timeout(30)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.StatusUpdate.WEB_APP_DATA,
            web_app_payment,
        )
    )

    app.add_error_handler(error_handler)

    print("💜 NEXI BOT ЗАПУЩЕН")
    print("💳 Заявки будут приходить владельцу")

    app.run_polling(
        drop_pending_updates=True,
        bootstrap_retries=-1,
    )


if __name__ == "__main__":
    main()
