import json
import sys
import time
import telebot
import threading
from api.bot_api import send_hello, get_request_distance_message, send_places, UserSession, get_places_to_send, \
    get_next_place_button
from geo.geo import Points, Point




bot = telebot.TeleBot('6620391167:AAGVt-OgRgKRvmVTjxkfgtcEN21b2NkLkTY')


session_dict = {}




if len(sys.argv) > 1 and not str(sys.argv[1]):
    with open('/tourist_bot/bot/jsfile/test.js', encoding="utf-8") as f:
        js = json.load(f)
else:
    with open('/tourist_bot/bot/jsfile/test.js', encoding="utf-8") as f:
        js = json.load(f)



dict = {}
point_arr = []
for e in js:
    coordinates = e.get('centroid_coordinates')

    point = Point(coordinates[0], coordinates[1], e.get("@id"))
    point_arr.append(point)

points = Points(point_arr)




point_to_place = {}

for item in js:
    key = (item.get('@id'))
    tourism = item.get('tourism')
    name = item.get('name')
    if name == "":
        name = item.get('alt_name')
    artwork_type = item.get('artwork_type')
    website = item.get('website')
    centroid_coordinates = item.get('centroid_coordinates')

    if key and centroid_coordinates:
        point_to_place[key] = tourism, name, artwork_type, website, centroid_coordinates


def clean_session_dict():
    while True:
        current_time = time.time()
        keys_to_remove = []
        for user_id, session in session_dict.items():
            if current_time - session.timestamp > 1200:
                keys_to_remove.append(user_id)

        for user_id in keys_to_remove:
            session_dict.pop(user_id)

        time.sleep(1200)


# Создайте и запустите поток для очистки session_dict
cleaning_thread = threading.Thread(target=clean_session_dict)
cleaning_thread.daemon = True  # Поток будет завершен при завершении основной программы
cleaning_thread.start()


@bot.message_handler(commands=['start'])
def start(message):
    print(f"received new user {message}")
    user_id = message.from_user.id
    chat_id = message.chat.id
    bot_message = send_hello(chat_id)

    session_dict.update({user_id: UserSession(0, 0, 0)})

    print(f"send to new user {message}")
    bot.send_message(chat_id=bot_message.chat_id, text=bot_message.text, reply_markup=bot_message.reply_markup)


@bot.message_handler(content_types=['location'])
def get_location(message):
    print(f"received location {message}")
    user_id = message.from_user.id
    chat_id = message.chat.id
    session_dict.update({user_id: UserSession(0, 0, 0)})
    session = session_dict.get(user_id)
    print(f'added user {user_id}')
    session.lat = message.location.latitude
    session.lon = message.location.longitude
    bot_message = get_request_distance_message(chat_id)
    print(f"send request distance {bot_message}")

    bot.send_message(chat_id=bot_message.chat_id, text=bot_message.text, reply_markup=bot_message.reply_markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'Next')
def callback_inline(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    session = session_dict.get(user_id)
    session.distance = call.data
    messages = get_places_to_send(chat_id, points, point_to_place, session)
    if not session.points:
        bot.send_message(chat_id=chat_id, text="Достопримечательности в этом радиусе закончились")
        bot_message = get_request_distance_message(chat_id)
        bot.send_message(chat_id=bot_message.chat_id, text=bot_message.text, reply_markup=bot_message.reply_markup)
    else:
        for m in messages:
            bot.send_message(
                chat_id=m.chat_id,
                text=m.text,
                parse_mode=m.parse_mode
            )
    if not session.points:
        bot.send_message(chat_id=chat_id, text="Достопримечательности в этом радиусе закончились")
        bot_message = get_request_distance_message(chat_id)
        bot.send_message(chat_id=bot_message.chat_id, text=bot_message.text, reply_markup=bot_message.reply_markup)
    else:
        bot_message = get_next_place_button(chat_id)
        bot.send_message(chat_id=bot_message.chat_id, text=bot_message.text, reply_markup=bot_message.reply_markup)



@bot.callback_query_handler(func=lambda callback: callback.data in ['50', '150', '250', '500'])
def callback_inline(call):
    print(f"received pressed btn {call}")
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    session = session_dict.get(user_id)

    session.distance = call.data
    messages = send_places(chat_id, points, point_to_place, session)


    print(f"send places {messages}")

    if not messages:
        bot.send_message(chat_id, "Достопримечательностей не найдено, поробуйте изменить радиус поиска или выбрать другую геолакацию")
        bot_message = get_request_distance_message(chat_id)
        bot.send_message(chat_id=bot_message.chat_id, text=bot_message.text, reply_markup=bot_message.reply_markup)
    else:
        for m in messages:
            bot.send_message(
                chat_id=m.chat_id,
                text=m.text,
                parse_mode=m.parse_mode
            )
        bot_message = get_next_place_button(chat_id)
        bot.send_message(chat_id=bot_message.chat_id, text=bot_message.text, reply_markup=bot_message.reply_markup)


bot.polling(none_stop=True, interval=1)