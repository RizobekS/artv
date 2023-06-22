from django.contrib import admin

from billing.models import PaymeModel, ApelsinModel


class PaymeModelAdmin(admin.ModelAdmin):
    list_display = (
        'paycom_transaction_id',
        'paycom_time',
        'paycom_time_datetime',
        'create_time',
        'perform_time',
        'cancel_time',
        'user',
        'order',
        'amount',
        'reason',
        'status_payment'
    )
    readonly_fields = (
        'paycom_transaction_id',
        'paycom_time',
        'paycom_time_datetime',
        'create_time',
        'perform_time',
        'cancel_time',
        'user',
        'order',
        'amount',
        'reason',
        'status_payment'
    )


class ApelsinModelAdmin(admin.ModelAdmin):
    list_display = (
        'transaction_id',
        'create_time',
        'perform_time',
        'cancel_time',
        'user',
        'order',
        'amount',
    )
    readonly_fields = (
        'transaction_id',
        'create_time',
        'perform_time',
        'cancel_time',
        'user',
        'order',
        'amount',
    )


admin.site.register(PaymeModel, PaymeModelAdmin)
admin.site.register(ApelsinModel, ApelsinModelAdmin)

