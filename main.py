import random
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Словарь для хранения подписок пользователей
subscriptions = {}

# Список советов по категориям
advice = {
    'health': ["Занимайтесь спортом регулярно.", "Пейте достаточно воды."],
    'personal_growth': ["Читайте книги каждый день.", "Ставьте перед собой цели."],
    'finance': ["Составьте бюджет.", "Инвестируйте в свое образование."],
    'relationships': ["Уделяйте время своим близким.", "Будьте внимательны к другим."]
}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используйте /subscribe, чтобы получать ежедневные советы.')


def subscribe(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Здоровье", callback_data='health')],
        [InlineKeyboardButton("Личностный рост", callback_data='personal_growth')],
        [InlineKeyboardButton("Финансы", callback_data='finance')],
        [InlineKeyboardButton("Отношения", callback_data='relationships')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите категорию:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    category = query.data
    user_id = query.from_user.id

    subscriptions[user_id] = category
    query.edit_message_text(text=f"Вы подписались на советы по категории: {category}.")


def send_daily_advice(context: CallbackContext) -> None:
    for user_id, category in subscriptions.items():
        advice_message = random.choice(advice[category])
        context.bot.send_message(chat_id=user_id, text=advice_message)


def unsubscribe(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in subscriptions:
        del subscriptions[user_id]
        update.message.reply_text('Вы отписались от получения советов.')
    else:
        update.message.reply_text('Вы не подписаны на советы.')


def main() -> None:
    updater = Updater("YOUR_TOKEN")  # Замените YOUR_TOKEN на токен вашего бота

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("subscribe", subscribe))
    updater.dispatcher.add_handler(CommandHandler("unsubscribe", unsubscribe))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # Запланировать отправку советов каждый день
    job_queue = updater.job_queue
    job_queue.run_daily(send_daily_advice, time=datetime.time(hour=9, minute=0))  # Время отправки

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
