'''CALLBACKLARNI ILADIGAN HANDLERLAR'''
from telebot.types import CallbackQuery
from data.loader import bot, db
from keyboards.default import main_menu
from keyboards.inline import get_products_list_buttons, \
    get_categories_buttons, get_products_by_pagination, \
    get_product_control_buttons, show_card_buttons
from states.states import CardState
from shipping_data.shipping_detail import generate_product_invoice


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def reaction_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Asosiy menu", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: "category|" in call.data)
def reaction_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    category_id = call.data.split('|')[1]
    # products = db.select_products_by_category_id(category_id)

    bot.delete_message(chat_id, call.message.message_id)
    # bot.delete_message(chat_id, call.message.message_id - 1)
    bot.send_message(chat_id, "Mahsulotlar", reply_markup=get_products_by_pagination(category_id))


@bot.callback_query_handler(func=lambda call: call.data == 'back_categories')
def reaction_back_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    categories = db.select_all_categories()

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Katalog", reply_markup=get_categories_buttons(categories))


@bot.callback_query_handler(func=lambda call: "next_page|" in call.data)
def reaction_to_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id

    elements = call.message.reply_markup.keyboard[-2]
    category_id = int(call.data.split('|')[1])
    page = None
    for element in elements:
        # print(element)
        if element.callback_data == 'current_page':
            page = int(element.text)
    page += 1
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Mahsulotlar", reply_markup=get_products_by_pagination(category_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page')
def reaction_to_current_page(call: CallbackQuery):
    elements = call.message.reply_markup.keyboard[-2]

    page = None
    for element in elements:
        if element.callback_data == 'current_page':
            page = int(element.text)

    bot.answer_callback_query(call.id, f"Siz {page} - sahifadasiz!", show_alert=True)


@bot.callback_query_handler(func=lambda call: "product|" in call.data)
def reaction_to_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    product_id = int(call.data.split('|')[1])
    product = db.get_product_by_id(product_id)
    title, link, price, image, cat_id = product
    # print(cat_id)

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_photo(chat_id, image, caption=f"""
<b>{title}</b>
Narhi: <i>{price}</i>
<a href="{link}">Batafsil ma'lumot</a>
""", parse_mode='html', reply_markup=get_product_control_buttons(cat_id, product_id))


@bot.callback_query_handler(func=lambda call: call.data in ['plus', 'minus'])
def reaction_to_plus_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id, cache_time=1)

    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    category_id = int(call.message.reply_markup.keyboard[2][0].callback_data.split('|')[1])
    product_id = call.message.reply_markup.keyboard[1][0].callback_data.split('|')[1]

    if call.data == 'plus':
        quantity += 1
        bot.edit_message_reply_markup(chat_id, call.message.message_id, call.id,
                                      reply_markup=get_product_control_buttons(category_id, product_id, quantity))
    else:
        if quantity > 1:
            quantity -= 1
            bot.edit_message_reply_markup(chat_id, call.message.message_id, call.id,
                                          reply_markup=get_product_control_buttons(category_id, product_id, quantity))


@bot.callback_query_handler(func=lambda call: call.data == "quantity")
def reaction_to_quantity(call: CallbackQuery):
    quantity = call.message.reply_markup.keyboard[0][1].text
    bot.answer_callback_query(call.id, f"Jami: {quantity} ta")


@bot.callback_query_handler(func=lambda call: 'add|' in call.data)
def reaction_to_add_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    product_id = call.data.split('|')[1]
    product = db.get_product_by_id(product_id)
    product_name = product[0]
    product_price = product[2]
    quantity = int(call.message.reply_markup.keyboard[0][1].text)

    bot.set_state(from_user_id, CardState.card, chat_id)
    with bot.retrieve_data(from_user_id, chat_id) as data:
        if data.get('card'):
            data['card'][product_name] = {
                'product_id': product_id,
                'quantity': quantity,
                'price': product_price
            }
        else:
            data['card'] = {
                product_name: {
                    'product_id': product_id,
                    'quantity': quantity,
                    'price': product_price
                }
            }
        bot.answer_callback_query(call.id, "Mahsulot savatga qo'shildi!")



@bot.callback_query_handler(func=lambda call: call.data =="show_card")
def reaction_to_show_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id


    with bot.retrieve_data(from_user_id, chat_id) as data:
        result = get_text_reply_markup(data)

    text = result['text']
    markup = result['markup']

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: "remove|" in call.data)
def reaction_to_remove(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    product_id = call.data.split('|')[1]


    with bot.retrieve_data(from_user_id, chat_id) as data:
        keys = [product_name for product_name in data['card'].keys()]
        for key in keys:
            if data['card'][key]['product_id'] == product_id:
                del data['card'][key]

    result = get_text_reply_markup(data)
    text = result['text']
    markup = result['markup']
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text, reply_markup=markup)


def get_text_reply_markup(data):
    text = 'Savat:\n'
    total_price = 0
    for product_name, item in data['card'].items():
        product_price = item['price']
        quantity = item['quantity']
        price = quantity * int(product_price)
        total_price += price
        text += f'''{product_name}
    Narxi: {quantity} * {product_price} = {price} so'm\n'''

    if total_price == 0:
        text = "Sizning savatingiz bo'sh!"
        markup = main_menu()
    else:
        text += f"\nUmumiy narx: {total_price} so'm"
        markup = show_card_buttons(data['card'])

    return {'markup': markup, 'text': text, 'total_price': total_price}

@bot.callback_query_handler(func=lambda call: call.data == 'clear_card')
def reaction_to_clear_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_state(user_id, chat_id)
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Sizning savatingiz tozalandi!", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: call.data == 'submit')
def submit_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    with bot.retrieve_data(user_id, chat_id) as data:
        bot.send_invoice(chat_id, **generate_product_invoice(data['card']).generate_invoice(),
                         invoice_payload='shop_bot')

