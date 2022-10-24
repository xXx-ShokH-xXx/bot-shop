from telebot.types import ShippingQuery, PreCheckoutQuery
from data.loader import bot, db
from shipping_data.shipping_detail import *


@bot.shipping_query_handler(func=lambda query: True)
def choose_shipping(query: ShippingQuery):
    if query.shipping_address.country_code != 'UZ':
        bot.answer_shipping_query(shipping_query_id=query.id, ok=True,
                                  error_message="Yetkazib berish faqat O'zbekiston bo'ylab mavjud!")

    elif query.shipping_address.city.lower() in ['toshkent', 'tashkent', 'тошкент', 'ташкент']:
        bot.answer_shipping_query(shipping_query_id=query.id, ok=True,
                                  shipping_options=[EXPRESS_SHIPPING, REGULAR_SHIPPING, PICKUP_SHIPPING])

    elif query.shipping_address.city.lower() not in ['toshkent', 'tashkent', 'тошкент', 'ташкент']:
        bot.answer_shipping_query(shipping_query_id=query.id, ok=True,
                                  shipping_options=[REGION_SHIPPING])
@bot.pre_checkout_query_handler(func=lambda pre_checkout: True)
def checkout(pre_checkout_query: PreCheckoutQuery):
    user_id = pre_checkout_query.from_user.id
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message='TEST')
    bot.send_message(user_id, "Xaridingiz uchun raxmat!")
    with bot.retrive_data(user_id, user_id) as data:
        customer_full_name = db.check_user_info(user_id)[0]
        create_order = db.create_order(customer_full_name)
        order_id = create_order[0]
        for item in data['card']:
            product_name = item
            product_quantity = data['card'][item]['quantity']
            product_price = data['card'][item]['price']
            total_price = int(product_quantity) * int(product_price) * 100

            db.create_table_order_item(product_name, product_quantity, product_price, total_price, order_id)


    bot.delete_state(user_id, user_id)
