from telebot import TeleBot
import buttons as bt
from geopy import Photon
geolocator = Photon(user_agent="geo_locator", timeout=10)

# создание объекта нашего
bot = TeleBot(token="TOKEN")
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
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

# поддержание запуска бота
bot.infinity_polling()
