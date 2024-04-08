import logging

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import ApplicationBuilder
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove

BOT_TOKEN = "6674667829:AAFJX5J8TLRjbLYaLL4nbRkXmYVZsYr6pTo"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['/address'],
                  ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Помогу вам определится с выбором страны, в которую вы захотите поехать, а также расскажу о её достопримечательностях",
        reply_markup=markup
    )

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
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("address", address))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
