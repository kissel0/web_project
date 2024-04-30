import logging
import sys
import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, ConversationHandler, filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove

BOT_TOKEN = "6674667829:AAFJX5J8TLRjbLYaLL4nbRkXmYVZsYr6pTo"
URL = 'https://api.telegram.org/bot'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['/address'],
                  ['/help']]

reply_keyboard1 = [['развлечения'], ['природа'], ['еда'], ['культура']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup1 = ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True)


def get_culture_info(lat, lon):
    culture_info = set()
    url = f"https://api.geoapify.com/v2/places?categories=entertainment.culture&filter=circle:{lon},{lat},50000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response = requests.get(url).json()
    for i in response['features']:
        try:
            culture_info.add(
                (i['properties']['name'], i['properties']['website'], i['properties']['lon'], i['properties']['lat']))
        except:
            pass
    return culture_info


def get_nuturel_info(lat, lon):
    f = set()
    cat = [('entertainment.zoo', 3), ('entertainment.planetarium', 3), ('natural', 10)]
    for i in cat:
        url = f"https://api.geoapify.com/v2/places?categories={i[0]}&filter=circle:{lon},{lat},50000&bias=proximity:{lon},{lat}&limit={i[-1]}&apiKey=23b70e7a81254e459c88d574598a37ab"
        response = requests.get(url)
        info = response.json()
        for j in info['features']:
            try:
                f.add((j['properties']['name'], j['properties']['website'], j['properties']['lon'],
                       j['properties']['lat']))
            except:
                pass
    return f


def get_food_info(lat, lon):
    food_info = set()
    url = f"https://api.geoapify.com/v2/places?categories=catering.restaurant&filter=circle:{lon},{lat},10000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response = requests.get(url)
    for i in response.json()['features']:
        try:
            food_info.add(
                (i['properties']['name'], i['properties']['website'], i['properties']['lon'], i['properties']['lat']))
        except:
            pass
    url_2 = f"https://api.geoapify.com/v2/places?categories=catering.fast_food&filter=circle:{lon},{lat},10000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response_2 = requests.get(url_2)
    for j in response_2.json()['features']:
        try:
            food_info.add(
                (j['properties']['name'], j['properties']['website'], j['properties']['lon'], j['properties']['lat']))
        except:
            pass
    url_3 = f"https://api.geoapify.com/v2/places?categories=catering.cafe&filter=circle:{lon},{lat},10000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response_3 = requests.get(url_3)
    for l in response_3.json()['features']:
        try:
            food_info.add(
                (l['properties']['name'], l['properties']['website'], l['properties']['lon'], l['properties']['lat']))
        except:
            pass
    return food_info


def get_entertainment_info(lat, lon):
    entertainment_info = set()
    url = f"https://api.geoapify.com/v2/places?categories=entertainment.cinema&filter=circle:{lon},{lat},10000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response = requests.get(url)
    for j in response.json()['features']:
        try:
            entertainment_info.add(
                (j['properties']['name'], j['properties']['website'], j['properties']['lon'], j['properties']['lat']))
        except:
            pass
    url_2 = f"https://api.geoapify.com/v2/places?categories=entertainment.water_park&filter=circle:{lon},{lat},10000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response_2 = requests.get(url_2)
    for i in response_2.json()['features']:
        try:
            entertainment_info.add(
                (i['properties']['name'], i['properties']['website'], i['properties']['lon'], i['properties']['lat']))
        except:
            pass
    return entertainment_info


async def start(update, context):
    await update.message.reply_text(
        "Я бот-справочник. Помогу вам определится с местом, в которое можно сходить, если не знаете, что делать\n"
        "Для этого выполните несколько действий, пожалуйста!\n"
        "Вы можете закончить с этим, послав команду /stop.\n"
        "Отправте пожалуйста свою геопозицию!❤️", reply_markup=ReplyKeyboardRemove()
    )
    return 1


async def receive_location(update, context):
    locat = update.message.location
    context.user_data['locality'] = update.message.text
    loc = str(locat).lstrip('Location').strip('()').split('=')
    del loc[0]
    l = ' '.join(loc).split(', longitude ')
    context.user_data['locality'] = (float(l[0]), float(l[1]))
    await update.message.reply_text("Мы нашли ближайшие к вам места, в которые вы можете сходить.\n"
                                    "Выберите пожалуйста категорию места",
                                    reply_markup=markup1)
    return 2


async def second_response(update, context):
    # Ответ на второй вопрос.
    # Мы можем его сохранить в базе данных или переслать куда-либо.
    weather = update.message.text
    locat = context.user_data['locality']
    flag = True
    if weather == 'развлечения':
        entert_lst = list(get_entertainment_info(locat[0], locat[-1]))
        print(entert_lst)
        map_request = f"http://static-maps.yandex.ru/1.x/?pt={locat[-1]},{locat[0]},home~{entert_lst[0][2]},{entert_lst[0][3]},pm2gnm~{entert_lst[1][2]},{entert_lst[1][3]},pm2rdm~{entert_lst[2][2]},{entert_lst[2][3]},pm2lbm&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        await update.message.reply_photo(map_file)
        await update.message.reply_text(f'Вот несколько развлекательных мест для вас:\n'
                                        f'🟢{entert_lst[0][0]}\n'
                                        f'  {entert_lst[0][1]}\n'
                                        f'🔴{entert_lst[1][0]}\n'
                                        f'  {entert_lst[1][1]}\n'
                                        f'🔵{entert_lst[2][0]}\n'
                                        f'  {entert_lst[2][1]}\n')

    elif weather == 'природа':
        nature_lst = list(get_nuturel_info(locat[0], locat[-1]))
        map_request = f"http://static-maps.yandex.ru/1.x/?pt={locat[-1]},{locat[0]},home~{nature_lst[0][2]},{nature_lst[0][3]},pm2gnm~{nature_lst[1][2]},{nature_lst[1][3]},pm2rdm~{nature_lst[2][2]},{nature_lst[2][3]},pm2lbm&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        await update.message.reply_photo(map_file)
        await update.message.reply_text(f'Вот несколько мест, связанных с природой, для вас:\n'
                                        f'🟢{nature_lst[0][0]}\n'
                                        f'  {nature_lst[0][1]}\n'
                                        f'🔴{nature_lst[1][0]}\n'
                                        f'  {nature_lst[1][1]}\n'
                                        f'🔵{nature_lst[2][0]}\n'
                                        f'  {nature_lst[2][1]}\n'
                                        )
    elif weather == 'еда':
        eat_lst = list(get_food_info(locat[0], locat[-1]))
        map_request = f"http://static-maps.yandex.ru/1.x/?pt={locat[-1]},{locat[0]},home~{eat_lst[0][2]},{eat_lst[0][3]},pm2gnm~{eat_lst[1][2]},{eat_lst[1][3]},pm2rdm~{eat_lst[2][2]},{eat_lst[2][3]},pm2lbm&l=map"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        await update.message.reply_photo(map_file)
        await update.message.reply_text(f'Вот несколько мест, где вы сможете поесть:\n'
                                        f'🟢{eat_lst[0][0]}\n'
                                        f'  {eat_lst[0][1]}\n'
                                        f'🔴{eat_lst[1][0]}\n'
                                        f'  {eat_lst[1][1]}\n'
                                        f'🔵{eat_lst[2][0]}\n'
                                        f'  {eat_lst[2][1]}\n')
    elif weather == 'культура':
        cultur_lst = list(get_culture_info(locat[0], locat[-1]))
        map_request = f"http://static-maps.yandex.ru/1.x/?pt={locat[-1]},{locat[0]},home~{cultur_lst[0][2]},{cultur_lst[0][3]},pm2gnm~{cultur_lst[1][2]},{cultur_lst[1][3]},pm2rdm~{cultur_lst[2][2]},{cultur_lst[2][3]},pm2lbm&l=map"
        response = requests.get(map_request)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        await update.message.reply_photo(map_file)
        await update.message.reply_text(f'Вот несколько мест, где вы сможете поесть:\n'
                                        f'🟢{cultur_lst[0][0]}\n'
                                        f'  {cultur_lst[0][1]}\n'
                                        f'🔴{cultur_lst[1][0]}\n'
                                        f'  {cultur_lst[1][1]}\n'
                                        f'🔵{cultur_lst[2][0]}\n'
                                        f'  {cultur_lst[2][1]}\n')
    else:
        flag = False
        await update.message.reply_text(
            "Вы ввели не то, что нужно. Попробуйте ещё раз!")
    logger.info(weather)
    if flag:
        await update.message.reply_text("Если вы нашли то, что вы хотели то введите команду /stop.",
                                        reply_markup=markup1)


async def stop(update, context):
    await update.message.reply_text("Всего доброго!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


async def help(update, context):
    await update.message.reply_text(
        "Я бот справочник.")


def main():
    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(None, receive_location))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("close", close_keyboard))
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
