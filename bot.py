from telebot import TeleBot
import buttons as bt
from geopy import Photon
import database as db
admins_group = -4661054301
geolocator = Photon(user_agent="geo_locator", timeout=10)
# db.add_product("Бургер", 30000.00, "лучший бургер", 10, "https://www.gazeta.uz/media/img/2017/10/8NWCAY15072899796600_l.jpg")
# db.add_product("Чизбургер", 35000.00, "лучший чизбургер", 10, "https://www.gazeta.uz/media/img/2017/10/8NWCAY15072899796600_l.jpg")
# db.add_product("Хот-дог", 25000.00, "лучший хот-дог", 0, "https://www.gazeta.uz/media/img/2017/10/8NWCAY15072899796600_l.jpg")
users = {}
# создание объекта нашего
bot = TeleBot(token="7630204824:AAFYX9Yfh3tg9Mg357ZvlAgHZEp-ZMfu8m0")
@bot.message_handler(commands=["start", "admin"])
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
@bot.callback_query_handler(lambda call: call.data in ["back", "cart", "plus", "minus",
                                                       "to_cart", "back_product", "cart",
                                                       "clear_cart", "order"])
def calls(call):
    user_id = call.message.chat.id
    if call.data == "back":
        bot.send_message(user_id, "Меню: ", reply_markup=bt.main_menu_bt())
    elif call.data == "plus":
        current_amount = users.get(user_id).get("pr_count")
        users[user_id]["pr_count"] += 1
        bot.edit_message_reply_markup(user_id, call.message.id,
                                      reply_markup=bt.plus_or_minus_in(plus_or_minus="plus",current_amount=current_amount))
    elif call.data == "minus":
        current_amount = users.get(user_id).get("pr_count")
        if current_amount > 1:
            users[user_id]["pr_count"] -= 1
            bot.edit_message_reply_markup(user_id, call.message.id,
                                          reply_markup=bt.plus_or_minus_in(plus_or_minus="minus",current_amount=current_amount))
    elif call.data == "to_cart":
        db.add_to_cart(user_id, users[user_id]["pr_id"], users[user_id]["pr_name"],
                       users[user_id]["pr_price"], users[user_id]["pr_count"])
        users.pop(user_id)
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Продукт успешно добавлен в корзину.\n"
                                  "Желаете что-нибудь еще?: ", reply_markup=bt.product_in(all_products))
    elif call.data == "back_product":
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт: ", reply_markup=bt.product_in(all_products))
    elif call.data == "cart":
        cart = db.get_user_cart(user_id)
        full_text = "Ваша корзина: \n"
        count = 0
        total_price = 0
        for product in cart:
            count += 1
            full_text += f"{count}. {product[0]} x {product[1]} = {product[2]}\n"
            total_price += product[2]
        full_text += f"Итоговая сумма: {total_price} сум"
        cart_info = db.get_cart_id_name(user_id)
        bot.send_message(user_id, full_text, reply_markup=bt.cart_in(cart_info))
    elif call.data == "clear_cart":
        db.delete_user_cart(user_id)
        bot.delete_message(user_id, call.message.message_id)
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Корзина очищена. Желаете что-нибудь заказать?: ",
                         reply_markup=bt.product_in(all_products))
    elif call.data == "order":
        cart = db.get_user_cart(user_id)
        full_text = f"Новый заказ от пользователя {user_id}: \n"
        count = 0
        total_price = 0
        for product in cart:
            count += 1
            full_text += f"{count}. {product[0]} x {product[1]} = {product[2]}\n"
            total_price += product[2]
        full_text += f"Итоговая сумма: {total_price} сум"
        bot.delete_message(user_id, call.message.message_id)
        db.delete_user_cart(user_id)
        bot.send_message(admins_group, full_text)
        bot.send_message(user_id, "Ваш заказ принят. Ожидайте", reply_markup=bt.main_menu_bt())



@bot.callback_query_handler(lambda call: "prod_" in call.data)
def get_prod_info(call):
    user_id = call.message.chat.id
    bot.delete_message(user_id, call.message.message_id)
    product_id = int(call.data.replace("prod_", ""))
    product_info = db.get_exact_product(product_id)
    # сохраняем информацию о количество выбранного продукта во временное хранилище
    users[user_id] = {"pr_id": product_id, "pr_name": product_info[0],
                      "pr_count": 1, "pr_price": product_info[1]}
    bot.send_photo(chat_id=user_id, photo=product_info[3], caption=f"{product_info[0]}\n"
                                                                   f"Цена: {product_info[1]} сум\n"
                                                                   f"Описание: {product_info[2]}",
                   reply_markup=bt.plus_or_minus_in())
@bot.callback_query_handler(lambda call: "delete_" in call.data)
def delete_prod_cart(call):
    user_id = call.message.chat.id
    product_id = int(call.data.replace("delete_", ""))
    db.delete_exact_product_from_cart(user_id, product_id)
    cart = db.get_user_cart(user_id)
    full_text = "Ваша корзина: \n"
    count = 0
    total_price = 0
    for product in cart:
        count += 1
        full_text += f"{count}. {product[0]} x {product[1]} = {product[2]}\n"
        total_price += product[2]
    full_text += f"Итоговая сумма: {total_price} сум"
    cart_info = db.get_cart_id_name(user_id)
    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                          text=full_text, reply_markup=bt.cart_in(cart_info))





@bot.message_handler(content_types=["text"])
def text_handler(message):
    print('сработа функция отлова сообщений с контентом "текст"')
    user_id = message.from_user.id
    if message.text == "🍴Меню":
        all_products = db.get_pr_id_name()
        bot.send_message(user_id, "Выберите продукт: ", reply_markup=bt.product_in(all_products))
    elif message.text == "✍️Отзыв":
        bot.send_message(user_id, "Напишите ваш отзыв: ")
    elif message.text == "🛒Корзина":
        bot.send_message(user_id, "Ваша корзина: ")
# поддержание запуска бота
bot.infinity_polling()
