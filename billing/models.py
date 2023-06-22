from django.db import models
from gallery.models import Order
from accounts.models import AuthUsers
from django.utils.translation import gettext_lazy as _


class ApelsinStatusChoices(models.TextChoices):
    APELSIN_SOLD = 'performed', _("Выполнен")
    APELSIN_CANCELED = 'canceled', _("Отменён")


class PaymeModel(models.Model):
    paycom_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    paycom_time = models.CharField(max_length=100, null=True, blank=True)
    paycom_time_datetime = models.DateTimeField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    perform_time = models.DateTimeField(null=True, blank=True)
    cancel_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(AuthUsers, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
    reason = models.IntegerField(null=True, blank=True)
    status_payment = models.IntegerField(default=0)


class ApelsinModel(models.Model):
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    perform_time = models.DateTimeField(null=True, blank=True)
    cancel_time = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(AuthUsers, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()



