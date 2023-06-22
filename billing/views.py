import os
import json
import base64
from datetime import datetime

from django.utils import timezone
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import renderer_classes
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from utils import currency_utils
from accounts.models import AuthUsers
from billing.models import PaymeModel, ApelsinModel
from gallery.models import Order, OrderStatusChoices, OrderItems, CartItemChoices, Cart


@csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def payme_view(request):
    if request.method == 'POST':
        # message = os.getenv('PAYME_TEST')
        # base64_string = base64.b64encode(message.encode('ascii')).decode("ascii")
        # nonauth = f"Basic {base64_string}"

        message2 = os.getenv('PAYME')
        base64_string2 = base64.b64encode(message2.encode('ascii')).decode("ascii")
        nonauth2 = f"Basic {base64_string2}"

        if 'HTTP_AUTHORIZATION' not in request.META or (
                request.META['HTTP_AUTHORIZATION'] != nonauth2):
            error_response = {
                "error": {
                    "code": -32504,
                    "message": "Недостаточно привелегий для выполнения метода.",
                },
            }
            return JsonResponse(error_response)

        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if 'method' not in body:
            error_response = {
                "error": {
                    "code": -32600,
                    "message": "В RPC-запросе отсутствуют обязательные поля "
                               "или тип полей не соответствует спецификации.",
                }
            }
            return JsonResponse(error_response)

        method = body['method']
        transaction_methods = (
            'CheckPerformTransaction',
            'PerformTransaction',
            'CreateTransaction',
            'CancelTransaction',
            'CheckTransaction',
            'GetStatement',
        )
        if method not in transaction_methods:
            error_response = {
                "error": -32601,
                "error_note": "Запрашиваемый метод не найден."
            }
            return JsonResponse(error_response)

        if method == 'CheckPerformTransaction':
            if 'params' not in body:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)

            params = body['params']
            if 'amount' not in params or 'account' not in params:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации. 3",
                    }
                }
                return JsonResponse(error_response)

            account = params['account']
            if 'email' not in account or 'phone' not in account or 'order_id' not in account:
                error_response = {
                    "error": {
                        "code": -31050,
                        "message": {"ru": "В account отсутствуют поля email/phone/order_id.",
                                    "en": "No fields email/phone/artworks_id/order_id.",
                                    "uz": "email/phone/artworks_id/order_id maydonlari yo'q"},
                    }
                }
                return JsonResponse(error_response)

            phone = account['phone'].replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
            if not AuthUsers.objects.filter(phone__contains=phone).exists():
                error_response = {
                    "error": {
                        "code": -31060,
                        "message": {"ru": "Отсутствует пользователь с таким номером.",
                                    "en": "No user with this phone.",
                                    "uz": "Bu telefon foydalanuvchisi yo'q."},
                    }
                }
                return JsonResponse(error_response)

            order_id = account['order_id']
            email = account['email']
            amount = params['amount'] / 100
            if not PaymeModel.objects.filter(order_id=order_id, user__phone=phone, user__email=email).exists():
                error_response = {
                    "error": {
                        "code": -31075,
                        "message": "Транзакция не найдена.",
                    },
                }
                return JsonResponse(error_response)

            payme = get_object_or_404(PaymeModel, order_id=order_id, user__phone=phone, user__email=email)
            if abs(amount - payme.order.total) > 1:
                error_response = {
                    "error": {
                        "code": -31001,
                        "message": f"Неверная сумма. {amount}, {payme.order.total}",
                    },
                }
                return JsonResponse(error_response)

            if payme.status_payment == 1:
                error_response = {
                    "error": {
                        "code": -31088,
                        "message": "Обрабатывается...",
                    },
                }
                return JsonResponse(error_response)
            elif payme.status_payment == 2:
                error_response = {
                    "error": {
                        "code": -31088,
                        "message": "Счет уже оплачен.",
                    },
                }
                return JsonResponse(error_response)
            elif payme.status_payment == -1:
                error_response = {
                    "error": {
                        "code": -31087,
                        "message": "Счет Отменен.",
                    },
                }
                return JsonResponse(error_response)
            error_response = {
                "result": {
                    "allow": True
                },
            }
            return JsonResponse(error_response)

        elif method == "CreateTransaction":
            if 'params' not in body:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)
            params = body['params']
            if 'amount' not in params or 'account' not in params or 'id' not in params or 'time' not in params:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)

            id = params['id']
            time = int(params['time'])
            account = params['account']
            if 'email' not in account and 'phone' not in account and 'order_id' not in account:
                error_response = {
                    "error": {
                        "code": -31050,
                        "message": {"ru": "В account отсутствуют поля email/phone/order_id.",
                                    "en": "No fields email/phone/order_id.",
                                    "uz": "email/phone/order_id"},
                    }
                }
                return JsonResponse(error_response)
            phone = account['phone'].replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
            if not AuthUsers.objects.filter(phone=phone).exists():
                error_response = {
                    "error": {
                        "code": -31060,
                        "message": {"ru": "Отсутствует пользователь с таким номером.",
                                    "en": "No user with this phone.",
                                    "uz": "Bu telefonli foydalanuvchi yo'q"},
                    }
                }
                return JsonResponse(error_response)

            email = account['email']
            order_id = account['order_id']
            amount = params['amount'] / 100
            if not PaymeModel.objects.filter(paycom_transaction_id=id).exists():
                if not PaymeModel.objects.filter(id=order_id, user__phone=phone, user__email=email).exists():
                    error_response = {
                        "error": {
                            "code": -31075,
                            "message": "Транзакция не найдена.",
                        },
                    }
                    return JsonResponse(error_response)
                payme = get_object_or_404(PaymeModel, id=order_id, user__phone=phone, user__email=email)
                if abs(amount - payme.order.total) > 1:
                    error_response = {
                        "error": {
                            "code": -31001,
                            "message": f"Неверная сумма 2. {amount}",
                        },
                    }
                    return JsonResponse(error_response)
                if payme.paycom_transaction_id is not None and payme.paycom_transaction_id != id:
                    error_response = {
                        "error": {
                            "code": -31080,
                            "message": "Вызов метода CreateTransaction с новой транзакцией.",
                        },
                    }
                    return JsonResponse(error_response)
                payme.paycom_transaction_id = id
                payme.create_time = timezone.now()
                payme.status_payment = 1
                timestmp = datetime.timestamp(payme.create_time) * 1000
                payme.save()
                error_response = {
                    "result": {
                        "create_time": timestmp,
                        "transaction": f"{payme.id}",
                        "state": 1
                    },
                }
                return JsonResponse(error_response)
            else:
                payme = get_object_or_404(PaymeModel, paycom_transaction_id=id)
                if amount != payme.order.total:
                    error_response = {
                        "error": {
                            "code": -31001,
                            "message": f"Неверная сумма 3. {amount}",
                        },
                    }
                    return JsonResponse(error_response)
                if payme.status_payment == 1:
                    addtime = payme.create_time + relativedelta(seconds=43200)
                    if timezone.now() > addtime:
                        payme.status_payment = -1
                        payme.reason = 4
                        payme.save()
                        error_response = {
                            "error": {
                                "code": -31008,
                                "message": "Невозможно выполнить операцию.",
                            },
                        }
                        return JsonResponse(error_response)
                    else:
                        timestmp = datetime.timestamp(payme.create_time) * 1000
                        error_response = {
                            "result": {
                                "create_time": timestmp,
                                "transaction": f"{payme.id}",
                                "state": 1
                            },
                        }
                        return JsonResponse(error_response)
                else:
                    error_response = {
                        "error": {
                            "code": -31008,
                            "message": "Невозможно выполнить операцию.",
                        },
                    }
                    return JsonResponse(error_response)

        elif method == 'CheckTransaction':
            if 'params' not in body:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)

            params = body['params']
            if 'id' not in params:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)

            id = params['id']
            if not PaymeModel.objects.filter(paycom_transaction_id=id).exists():
                error_response = {
                    "error": {
                        "code": -31003,
                        "message": "Транзакция не найдена.",
                    }
                }
                return JsonResponse(error_response)

            payme = get_object_or_404(PaymeModel, paycom_transaction_id=id)

            if payme.create_time is None:
                create_time = 0
            else:
                create_time = datetime.timestamp(payme.create_time) * 1000
            if payme.perform_time is None:
                perform_time = 0
            else:
                perform_time = datetime.timestamp(payme.perform_time) * 1000
            if payme.cancel_time is None:
                cancel_time = 0
            else:
                cancel_time = datetime.timestamp(payme.cancel_time) * 1000
            error_response = {
                "result": {
                    "create_time": create_time,
                    "transaction": f"{payme.id}",
                    "state": payme.status_payment,
                    "perform_time": perform_time,
                    "cancel_time": cancel_time,
                    "reason": payme.reason
                }
            }
            return JsonResponse(error_response)

        elif method == 'PerformTransaction':
            if 'params' not in body:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)
            params = body['params']
            if 'id' not in params:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)
            id = params['id']
            if not PaymeModel.objects.filter(paycom_transaction_id=id).exists():
                error_response = {
                    "error": {
                        "code": -31003,
                        "message": "Транзакция не найдена.",
                    }
                }
                return JsonResponse(error_response)

            payme = get_object_or_404(PaymeModel, paycom_transaction_id=id)
            if payme.status_payment == 1:
                addtime = payme.create_time + relativedelta(seconds=43200)
                if timezone.now() > addtime:
                    payme.status_payment = -1
                    payme.reason = 4
                    payme.save()
                    error_response = {
                        "error": {
                            "code": -31008,
                            "message": "Невозможно выполнить операцию.",
                        },
                    }
                    return JsonResponse(error_response)

                ordr_id = payme.order.id
                if Order.objects.filter(user__email__exact=payme.user.email,
                                        user__phone__exact=payme.user.phone).exists():
                    user_order = get_object_or_404(Order,
                                                   user__email=payme.user.email,
                                                   id=ordr_id)
                    user_order.status = OrderStatusChoices.ORDER_PAID
                    user_order.updated_at = timezone.now()
                    user_order.save()
                    payme.status_payment = 2
                    payme.perform_time = timezone.now()
                    perform_time = datetime.timestamp(payme.perform_time) * 1000
                    payme.save()
                    error_response = {
                        "result": {
                            "transaction": f"{payme.id}",
                            "perform_time": perform_time,
                            "state": 2
                        }
                    }
                    return JsonResponse(error_response)

            else:
                if payme.status_payment == 2:
                    perform_time = datetime.timestamp(payme.perform_time) * 1000
                    error_response = {
                        "result": {
                            "transaction": f"{payme.id}",
                            "perform_time": perform_time,
                            "state": 2
                        }
                    }
                    return JsonResponse(error_response)
                else:
                    error_response = {
                        "error": {
                            "code": -31008,
                            "message": "Невозможно выполнить операцию. "
                                       "Ошибка возникает если состояние транзакции, не позволяет выполнить операцию.",
                        },
                    }
                    return JsonResponse(error_response)

        elif method == 'CancelTransaction':
            if 'params' not in body:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)
            params = body['params']
            if 'id' not in params or 'reason' not in params:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)
            id = params['id']
            reason = int(params['reason'])
            if not PaymeModel.objects.filter(paycom_transaction_id=id).exists():
                error_response = {
                    "error": {
                        "code": -31003,
                        "message": "Транзакция не найдена.",
                    }
                }
                return JsonResponse(error_response)

            payme = get_object_or_404(PaymeModel, paycom_transaction_id=id)

            if payme.status_payment == 1:
                payme.status_payment = -1
                payme.reason = reason
                payme.cancel_time = timezone.now()
                cancel_time = datetime.timestamp(payme.cancel_time) * 1000
                payme.save()

                ordr_id = payme.order.id
                user_order = get_object_or_404(Order,
                                               user__email=payme.user.email,
                                               id=ordr_id)
                user_order.status = OrderStatusChoices.ORDER_PAID
                user_order.save()

                error_response = {
                    "result": {
                        "transaction": f"{payme.id}",
                        "cancel_time": cancel_time,
                        "state": payme.status_payment
                    }
                }
                return JsonResponse(error_response)

            elif payme.status_payment == 2:
                payme.status_payment = -2
                payme.reason = reason
                payme.cancel_time = timezone.now()
                cancel_time = datetime.timestamp(payme.cancel_time) * 1000
                payme.save()

                ordr_id = payme.order.id
                user_order = get_object_or_404(Order,
                                               user__email=payme.user.email,
                                               id=ordr_id)
                user_order.status = OrderStatusChoices.ORDER_PAID
                user_order.save()

                error_response = {
                    "result": {
                        "transaction": f"{payme.id}",
                        "cancel_time": cancel_time,
                        "state": payme.status_payment
                    }
                }
                return JsonResponse(error_response)
            else:
                cancel_time = datetime.timestamp(payme.cancel_time) * 1000
                error_response = {
                    "result": {
                        "transaction": f"{payme.id}",
                        "cancel_time": cancel_time,
                        "state": payme.status_payment
                    }
                }
                return JsonResponse(error_response)

        elif method == 'GetStatement':
            transactions = []
            if 'params' not in body:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)
            params = body['params']
            if 'from' not in params or 'to' not in params:
                error_response = {
                    "error": {
                        "code": -32600,
                        "message": "В RPC-запросе отсутствуют обязательные поля "
                                   "или тип полей не соответствует спецификации.",
                    }
                }
                return JsonResponse(error_response)
            from_time = int(params['from']) / 1000
            to_time = int(params['to']) / 1000
            fromtimemain = datetime.fromtimestamp(from_time)
            totimemain = datetime.fromtimestamp(to_time)
            payme = PaymeModel.objects.filter(create_time__isnull=False, create_time__gte=fromtimemain,
                                              create_time__lte=totimemain).order_by('create_time')
            for a in payme:
                if a.create_time is None:
                    create_time = 0
                else:
                    create_time = datetime.timestamp(a.create_time) * 1000
                if a.perform_time is None:
                    perform_time = 0
                else:
                    perform_time = datetime.timestamp(a.perform_time) * 1000
                if a.cancel_time is None:
                    cancel_time = 0
                else:
                    cancel_time = datetime.timestamp(a.cancel_time) * 1000
                ino = {
                    "id": f"{a.paycom_transaction_id}",
                    "time": create_time,
                    "amount": a.amount * 100,
                    "account": {
                        "email": f"{a.user.email}",
                        "phone": f"{a.user.phone}",
                        "order_id": f"{a.order.id}",
                    },
                    "create_time": create_time,
                    "perform_time": perform_time,
                    "cancel_time": cancel_time,
                    "transaction": f"{a.id}",
                    "state": a.status_payment,
                    "reason": a.reason,
                }
                transactions.append(ino)
            error_response = {
                "result": {
                    "transactions": transactions
                }
            }
            return JsonResponse(error_response)
    else:
        error_response = {
            "error": {
                "code": -32300,
                "message": "Метод запроса не POST.",
            },
        }
        return JsonResponse(error_response)


@login_required()
def payme_redirect_page(request):
    merchant_id = '6286315c72a6247c42008796'

    cart = Cart.objects.get(user__email=request.user.email)
    auth_user = AuthUsers.objects.get(email__exact=request.user.email)
    cart_items = cart.cart_items.filter(status=CartItemChoices.CART_CART)

    order_items = []
    total = 0
    for cart_item in cart_items:
        if cart_item.is_applied_art:
            if not cart_item.applied_art.price:
                messages.warning(
                    request, 'Цена не установлена для {}'.format(cart_item.applied_art))
                return redirect("general:cart_page")
            total += cart_item.applied_art.price
            order_items.append(OrderItems.objects.create(applied_art=cart_item.applied_art))
        else:
            if not cart_item.art_work.price:
                messages.warning(
                    request, 'Цена не установлена для {}'.format(cart_item.art_work))
                return redirect("general:cart_page")
            total += cart_item.art_work.price
            order_items.append(OrderItems.objects.create(
                art_work=cart_item.art_work))

    # exchanges to sum
    usd_exchange_rate = float(currency_utils.get_currencies()['$'])
    total = float(total) * usd_exchange_rate
    total = float("{:.2f}".format(total))

    try:
        order = Order.objects.create(
            user=auth_user,
            status=OrderStatusChoices.ORDER_PENDING,
            sub_total=total,
            total=total
        )
        order.works.add(*order_items)
        PaymeModel.objects.create(
            id=order.id,
            user=auth_user,
            order=order,
            amount=total
        )
    except Exception as e:
        messages.error(request, 'Заказ не был осуществлен')
        return redirect("general:order_page")

    total = int(total * 100)

    message = f'm={merchant_id};ac.order_id={order.id};ac.phone={auth_user.phone};ac.email={auth_user.email};a={total}'
    base64_string = base64.b64encode(message.encode('ascii')).decode("ascii")

    redirect_url = f"https://checkout.paycom.uz/{base64_string}"
    return HttpResponseRedirect(redirect_url)


@csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def apelsin_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if 'amount' not in body or \
                'transactionId' not in body or \
                'email' not in body or \
                'phone' not in body or \
                'order_id' not in body:
            error_response = {
                "status": False,
            }
            return JsonResponse(error_response)

        # checking whether a user with the given email and phone exists
        email = body['email']
        phone = body['phone']
        transaction_id = body['transactionId']
        if not AuthUsers.objects.filter(email=email, phone=phone).exists():
            error_response = {
                "status": False,
            }
            return JsonResponse(error_response)
        user = AuthUsers.objects.get(email=email, phone=phone)

        # checking whether user has orders with pending status
        order_id = body['order_id']
        if not Order.objects.filter(
                id=order_id,
                user__email=email,
                user__phone=phone,
                ).exists():
            error_response = {
                "status": False,
            }
            return JsonResponse(error_response)
        order = Order.objects.get(
            id=order_id,
            user__email=email,
            user__phone=phone,
            status=OrderStatusChoices.ORDER_PENDING
        )

        # checking whether we already have executed transaction with the given transaction_id
        if ApelsinModel.objects.filter(transaction_id__exact=transaction_id, user__email=email).exists():
            error_response = {
                "status": False,
            }
            return JsonResponse(error_response)

        # checking the given amount and recorded amount in our Order
        amount = body['amount'] / 100
        if order.total != amount:
            error_response = {
                "status": False,
            }
            return JsonResponse(error_response)

        # creating an order, if request passed all the checks
        ApelsinModel.objects.create(
            user=user,
            order=order,
            amount=amount,
            transaction_id=transaction_id,
            perform_time=timezone.datetime.today(),
        )
        order.status = OrderStatusChoices.ORDER_PAID
        order.save()

        response = {
            "status": True
        }
        return JsonResponse(response)

    else:
        response = {
            "status": False
        }
        return JsonResponse(response)


@login_required()
def apelsin_redirect_page(request):
    cash_id = '27dda36f2c4d44338b18b2396bf59a51'

    cart = Cart.objects.get(user__email=request.user.email)
    auth_user = AuthUsers.objects.get(email__exact=request.user.email)
    cart_items = cart.cart_items.filter(status=CartItemChoices.CART_CART)

    order_items = []
    total = 0
    for cart_item in cart_items:
        if cart_item.is_applied_art:
            if not cart_item.applied_art.price:
                messages.warning(
                    request, 'Цена не установлена для {}'.format(cart_item.applied_art))
                return redirect("general:cart_page")
            total += cart_item.applied_art.price
            order_items.append(OrderItems.objects.create(applied_art=cart_item.applied_art))
        else:
            if not cart_item.art_work.price:
                messages.warning(
                    request, 'Цена не установлена для {}'.format(cart_item.art_work))
                return redirect("general:cart_page")
            total += cart_item.art_work.price
            order_items.append(OrderItems.objects.create(
                art_work=cart_item.art_work))


    # exchanges to sum
    usd_exchange_rate = float(currency_utils.get_currencies()['$'])
    total = float(total) * usd_exchange_rate
    total = float("{:.2f}".format(total))

    try:
        order = Order.objects.create(
            user=auth_user,
            status=OrderStatusChoices.ORDER_PENDING,
            sub_total=total,
            total=total
        )
        order.works.add(*order_items)
        ApelsinModel.objects.create(
            id=order.id,
            user=auth_user,
            order=order,
            amount=total
        )
    except Exception as e:
        messages.error(request, 'Заказ не был осуществлен')
        return redirect("general:order_page")
    total = int(total * 100)
    message = f"cash={cash_id}&order_id={order.id}&phone={auth_user.phone}&email={auth_user.email}&amount={total}"
    # &redirectUrl={request.get_host()}{reverse('home_page')}/history/"

    redirect_url = f"https://payment.apelsin.uz/?{message}"
    return HttpResponseRedirect(redirect_url)

