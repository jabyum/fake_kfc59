from telebot import TeleBot
import buttons as bt
from geopy import Photon
import database as db
geolocator = Photon(user_agent="geo_locator", timeout=10)

# создание объекта нашего
bot = TeleBot(token="token")
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    checker = db.check_user(user_id)
    if checker == True:
        bot.send_message(user_id, "Меню: ", reply_markup=bt.main_menu_bt())
    elif checker == False:
        bot.send_message(user_id, "Добро пожаловать в бот доставки!\n\n"
                                  "Введите своё имя")
        # перекидываем пользователя на следующий этап (функция приема имени)
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    print(name)
    bot.send_message(user_id, "Отлично! Теперь поделитесь своими контактами",
                     reply_markup=bt.phone_number_bt())
    bot.register_next_step_handler(message, get_phone, name)
def get_phone(message, name):
    user_id = message.from_user.id
    # проверяем отправил ли пользователь контакт по кнопке
    if message.contact:
        phone_number = message.contact.phone_number
        print(phone_number)
        bot.send_message(user_id, "Отлично! Теперь отправьте локацию",
                         reply_markup=bt.location_bt())
        bot.register_next_step_handler(message, get_location, name, phone_number)
    # если отправил контакт не по кнопке возвращаем в эту же функцию
    else:
        bot.send_message(user_id, "Ошибка! Отправьте свои контакты по кнопке в меню",
                         reply_markup=bt.phone_number_bt())
        bot.register_next_step_handler(message, get_phone, name)
def get_location(message, name, phone_number):
    user_id = message.from_user.id
    location = message.location
    address = geolocator.reverse((location.latitude, location.longitude)).address
    print(name, phone_number, address)
    db.add_user(name, phone_number, user_id)
    bot.send_message(user_id, "Вы успешно прошли регистрацию.\n\n"
                              "Меню: ", reply_markup=bt.main_menu_bt())
@bot.callback_query_handler(lambda call: call.data in ["back", "cart"])
def calls(call):
    user_id = call.chat.id
    if call.data == "back":
        bot.send_message(user_id, "Меню: ", reply_markup=bt.main_menu_bt())
    elif call.data == "cart":
        bot.send_message(user_id, "Ваша корзина: ")
@bot.callback_query_handler(lambda call: "prod_" in call.data)
def get_prod_info(call):
    user_id = call.chat.id
    product_id = int(call.data.replace("prod_", ""))
    product_info = db.get



@bot.message_handler(content_types=["text"])
def text_handler(message):
    print('сработа функция отлова сообщений с контентом "текст"')
    user_id = message.from_user.id
    if message.text == "🍴Меню":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт: ", reply_markup=bt.product_in(all_products))
    elif message.text == "✍️Отзыв":
        bot .send_message(user_id, "Напишите ваш отзыв: ")
    elif message.text == "🛒Корзина":
        bot.send_message(user_id, "Ваша корзина: ")
# поддержание запуска бота
bot.infinity_polling()
