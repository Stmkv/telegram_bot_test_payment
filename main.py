import os
from telegram import Update, LabeledPrice
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from dotenv import load_dotenv


load_dotenv()

token = os.environ.get("TELEGRAM_TOKEN")
payment_provider_token = os.environ.get("PAYMENT_PROVIDER_TOKEN")


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Добро пожаловать! Для начала оплаты используйте\
                              команду /pay")


def pay(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    title = "Тестовая оплата"
    description = "Оплата услуг салона Beauty-City"
    payload = "Стрижка машинкой"
    currency = "RUB"
    prices = [LabeledPrice("Тестовая оплата", 10000)]  # Цена в копейках

    context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=payment_provider_token,
        currency=currency,
        prices=prices,
        start_parameter="test-payment",  # Уникальный параметр
        need_name=True,
        need_phone_number=True,
    )


def successful_payment_callback(update: Update, context: CallbackContext):
    update.message.reply_text("Платеж прошел успешно!")


def main() -> None:
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("pay", pay))
    dp.add_handler(MessageHandler(Filters.successful_payment,
                                  successful_payment_callback))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
