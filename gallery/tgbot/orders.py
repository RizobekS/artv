import datetime
from telebot import types

from ..models import Order, OrderStatusChoices


def get_data(chat_id, bot):
    # getting list of orders with "status" pending
    ten_minutes_ago = datetime.datetime.now() + datetime.timedelta(minutes=-10)

    if Order.objects.filter(status_en=OrderStatusChoices.ORDER_PENDING, created_at__gte=ten_minutes_ago).exists():
        date_message = f"—————\nТекущие заказы к: {datetime.datetime.now().strftime('%B %d %H:%M')}\n—————"
        bot.send_message(chat_id, date_message)

        orders = Order.objects.filter(status_en=OrderStatusChoices.ORDER_PENDING, created_at__gte=ten_minutes_ago)

        # in this gigantic loop we are getting info about each order with "status" pending and sending to the group
        for order in orders:
            order_id = order.id
            created_at = order.created_at.strftime('%B %d %Y %H:%M')
            full_name = f"{order.user.first_name} {order.user.last_name}"
            email = order.user.email
            phone = order.user.phone
            postcode = order.user.postcode
            address = f"{order.user.country}, {order.user.city}, {order.user.street}"
            discount = order.discount
            total_price = 0

            works_object = ''
            for work in order.works.all():
                name = work.art_work.name
                u_id = work.art_work.u_id
                price = work.art_work.price
                total_price += price
                works_object += f"\nНазвание картины: {name}\nАртикул: {u_id}\nЦена: {price}\n—————"

            # prepares data to be send
            order_info = f"ID заказа: {order_id}\n—————\nДата заказа: {created_at}\nАдрес: {address}\n" \
                         f"Почтовый Индекс: {postcode}\nE-mail: {email}\nТелефон: {phone}\n" \
                         f"Имя заказчика: {full_name}\nДисконт: {discount}\nСписок товаров:\n—————"
            order_info += works_object
            order_info += f"\nИтого: {total_price}\nСтатус: в ожидании\n"

            keyboard = [
                [types.InlineKeyboardButton("✅Обработать", callback_data='completed' + ' ' + str(order_id))],
                [types.InlineKeyboardButton("🚫Отменить", callback_data='canceled' + ' ' + str(order_id))]
            ]
            markup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id, order_info, reply_markup=markup)


# processes inline button clicks
def process_order(call, bot, chat_id):
    data, order_id = call.data.split(' ')
    edited_text = call.message.text
    editor_fullname = call.from_user.first_name + ' ' + call.from_user.last_name
    print(order_id)

    if data == 'completed':
        order = Order.objects.get(id=order_id, status_en=OrderStatusChoices.ORDER_PENDING)
        order.status_en = OrderStatusChoices.ORDER_COMPLETE
        order.status_uz = OrderStatusChoices.ORDER_COMPLETE
        order.status_ru = OrderStatusChoices.ORDER_COMPLETE
        order.status_zh_cn = OrderStatusChoices.ORDER_COMPLETE
        order.save()

        edited_text = edited_text[:-10] + f'✅Обработан - {editor_fullname}'
        bot.answer_callback_query(call.id, 'Обработан!')

    elif data == 'canceled':
        order = Order.objects.get(id=order_id, status_en=OrderStatusChoices.ORDER_PENDING)
        order.status_en = OrderStatusChoices.ORDER_CANCELED
        order.status_uz = OrderStatusChoices.ORDER_CANCELED
        order.status_ru = OrderStatusChoices.ORDER_CANCELED
        order.status_zh_cn = OrderStatusChoices.ORDER_CANCELED
        order.save()

        edited_text = edited_text[:-10] + f'🚫Отменён - {editor_fullname}'
        bot.answer_callback_query(call.id, 'Отменён!')

    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.id)
    bot.edit_message_text(text=edited_text, chat_id=chat_id, message_id=call.message.id)













