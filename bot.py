import logging
import time
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
)
import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove

BOT_TOKEN = "6674667829:AAFJX5J8TLRjbLYaLL4nbRkXmYVZsYr6pTo"
URL = 'https://api.telegram.org/bot'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['/address'],
                  ['/help']]

reply_keyboard1 = [['вариант1'], ['вариант2']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True)

lst = []


async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Помогу вам определится с выбором страны, в которую вы захотите поехать, а также расскажу о её достопримечательностях.\n"
        "Для этого пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "Отправте пожалуйста свою геопозицию!❤️"
        # reply_markup=markup1
    )
    return 1
def receive_location(update: Update, context: CallbackContext):
    lst.append(update.message.location)
    print(lst)



async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


async def address(update, context):
    await update.message.reply_text(
        "Адрес: г. Санкт-Петербург, Жемчужная плаза")


def main():
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # # Функция читает ответ на первый вопрос и задаёт второй.
            # 1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response)],
            # # Функция читает ответ на второй вопрос и завершает диалог.
            # 2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(conv_handler)
    # application.add_handler(CommandHandler('location', request_location))
    application.add_handler(MessageHandler(None, receive_location))
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
