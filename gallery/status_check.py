import time
import schedule

from gallery.models import (
    Works, Order,
    StatusChoices, OrderItemChoices, OrderStatusChoices
)


def main():
    def status_update():
        # orders with "pending" status
        if Order.objects.filter(status_en=OrderStatusChoices.ORDER_PENDING).exists():
            pending_orders = Order.objects.filter(status_en=OrderStatusChoices.ORDER_PENDING).order_by('created_at')
            for order in pending_orders:
                order_items = order.works.all()
                for order_item in order_items:
                    work = Works.objects.get(id=order_item.art_work_id)

                    order_item.status_en = OrderItemChoices.ORDER_PENDING
                    order_item.status_uz = OrderItemChoices.ORDER_PENDING
                    order_item.status_ru = OrderItemChoices.ORDER_PENDING
                    order_item.status_zh_cn = OrderItemChoices.ORDER_PENDING

                    work.status_en = StatusChoices.ORDERED
                    work.status_uz = StatusChoices.ORDERED
                    work.status_ru = StatusChoices.ORDERED
                    work.status_zh_cn = StatusChoices.ORDERED

                    work.shoppable = False

                    work.save()
                    order_item.save()

        # orders with "complete" status
        if Order.objects.filter(status_en=OrderStatusChoices.ORDER_COMPLETE).order_by('created_at').exists():
            complete_orders = Order.objects.filter(status_en=OrderStatusChoices.ORDER_COMPLETE).order_by('created_at')
            for order in complete_orders:
                order_items = order.works.all()
                for order_item in order_items:
                    work = Works.objects.get(id=order_item.art_work_id)

                    order_item.status_en = OrderItemChoices.ORDER_SOLD
                    order_item.status_uz = OrderItemChoices.ORDER_SOLD
                    order_item.status_ru = OrderItemChoices.ORDER_SOLD
                    order_item.status_zh_cn = OrderItemChoices.ORDER_SOLD

                    work.status_en = StatusChoices.SOLD
                    work.status_uz = StatusChoices.SOLD
                    work.status_ru = StatusChoices.SOLD
                    work.status_zh_cn = StatusChoices.SOLD
                    work.shoppable = False

                    work.save()
                    order_item.save()

        # orders with "canceled" status
        if Order.objects.filter(status_en=OrderStatusChoices.ORDER_CANCELED).order_by('created_at').exists():
            canceled_orders = Order.objects.filter(status_en=OrderStatusChoices.ORDER_CANCELED).order_by('created_at')
            for order in canceled_orders:
                order_items = order.works.all()
                for order_item in order_items:
                    work = Works.objects.get(id=order_item.art_work_id)

                    order_item.status_en = OrderItemChoices.ORDER_CANCELED
                    order_item.status_uz = OrderItemChoices.ORDER_CANCELED
                    order_item.status_ru = OrderItemChoices.ORDER_CANCELED
                    order_item.status_zh_cn = OrderItemChoices.ORDER_CANCELED

                    work.status_en = StatusChoices.NEW
                    work.status_uz = StatusChoices.NEW
                    work.status_ru = StatusChoices.NEW
                    work.status_zh_cn = StatusChoices.NEW
                    work.shoppable = True

                    work.save()
                    order_item.save()

        # orders with "returned" status
        if Order.objects.filter(status_en=OrderStatusChoices.ORDER_RETURNED).exists():
            returned_orders = Order.objects.filter(status_en=OrderStatusChoices.ORDER_RETURNED).order_by('created_at')
            for order in returned_orders:
                order_items = order.works.all()
                for order_item in order_items:
                    work = Works.objects.get(id=order_item.art_work_id)

                    order_item.status_en = OrderItemChoices.ORDER_CANCELED
                    order_item.status_uz = OrderItemChoices.ORDER_CANCELED
                    order_item.status_ru = OrderItemChoices.ORDER_CANCELED
                    order_item.status_zh_cn = OrderItemChoices.ORDER_CANCELED

                    work.status_en = StatusChoices.NEW
                    work.status_uz = StatusChoices.NEW
                    work.status_ru = StatusChoices.NEW
                    work.status_zh_cn = StatusChoices.NEW
                    work.shoppable = True

                    work.save()
                    order_item.save()

        # orders with "rejected" status
        if Order.objects.filter(status_en=OrderStatusChoices.ORDER_REJECTED).exists():
            rejected_orders = Order.objects.filter(status_en=OrderStatusChoices.ORDER_REJECTED).order_by('created_at')
            for order in rejected_orders:
                order_items = order.works.all()
                for order_item in order_items:
                    work = Works.objects.get(id=order_item.art_work_id)

                    order_item.status_en = OrderItemChoices.ORDER_CANCELED
                    order_item.status_uz = OrderItemChoices.ORDER_CANCELED
                    order_item.status_ru = OrderItemChoices.ORDER_CANCELED
                    order_item.status_zh_cn = OrderItemChoices.ORDER_CANCELED

                    work.status_en = StatusChoices.NEW
                    work.status_uz = StatusChoices.NEW
                    work.status_ru = StatusChoices.NEW
                    work.status_zh_cn = StatusChoices.NEW
                    work.shoppable = True

                    work.save()
                    order_item.save()

    schedule.every(2).minutes.do(status_update)
    while True:
        print("STARTED: Order status check")
        schedule.run_pending()
        time.sleep(10)

