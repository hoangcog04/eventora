from django.conf import settings
from django.db import models

from common.constants.choices import (
    CheckoutMethod,
    DeliveryMethod,
    OrderStatus,
    RefundRequestStatus,
)


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    event = models.ForeignKey("organizer.Event", null=True, on_delete=models.SET_NULL)
    coupon = models.ForeignKey("organizer.Coupon", null=True, on_delete=models.SET_NULL)
    order_sn = models.CharField(max_length=255, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    total_amount = models.DecimalField(max_digits=19, decimal_places=3)
    pay_amount = models.DecimalField(max_digits=19, decimal_places=3)
    coupon_amount = models.DecimalField(max_digits=19, decimal_places=3)
    checkout_method = models.PositiveSmallIntegerField(
        choices=CheckoutMethod.choices, default=CheckoutMethod.DEFAULT
    )
    status = models.PositiveSmallIntegerField(
        choices=OrderStatus.choices, default=OrderStatus.STARTED
    )
    delivery_method = models.PositiveSmallIntegerField(
        choices=DeliveryMethod.choices, default=DeliveryMethod.EMAIL
    )
    bill_receiver_email = models.CharField(max_length=255, blank=True)
    receiver_name = models.CharField(max_length=255, blank=True)
    payment_time = models.DateTimeField(null=True)
    delivery_time = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class OrderAttendee(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    ticket = models.ForeignKey("organizer.Ticket", null=True, on_delete=models.SET_NULL)
    ticket_stock = models.ForeignKey(
        "organizer.TicketStock", null=True, on_delete=models.SET_NULL
    )
    order_sn = models.CharField(max_length=255, blank=True)
    ticket_name = models.CharField(max_length=255, blank=True)
    ticket_pic = models.TextField(blank=True)
    ticket_price = models.DecimalField(max_digits=19, decimal_places=3)
    ticket_quantity = models.PositiveIntegerField()
    real_amount = models.DecimalField(max_digits=19, decimal_places=3)
    coupon_amount = models.DecimalField(max_digits=19, decimal_places=3)
    bill_receiver_email = models.CharField(max_length=255, blank=True)
    receiver_email = models.CharField(max_length=255, blank=True)
    refuned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class RefundRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)
    event = models.ForeignKey("organizer.Event", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    order_sn = models.CharField(max_length=255, blank=True)
    from_name = models.CharField(max_length=255, blank=True)
    from_email = models.CharField(max_length=255, blank=True)
    message = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    order_pay_amount = models.DecimalField(max_digits=19, decimal_places=3)
    checkout_method = models.PositiveSmallIntegerField(
        choices=CheckoutMethod.choices, default=CheckoutMethod.DEFAULT
    )
    delivery_method = models.PositiveSmallIntegerField(
        choices=DeliveryMethod.choices, default=DeliveryMethod.EMAIL
    )
    status = models.PositiveSmallIntegerField(
        choices=RefundRequestStatus.choices, default=RefundRequestStatus.PENDING
    )
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class RefundItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    refund_request = models.ForeignKey(
        RefundRequest, null=True, on_delete=models.SET_NULL
    )
    ticket = models.ForeignKey("organizer.Ticket", null=True, on_delete=models.SET_NULL)
    ticket_name = models.CharField(max_length=255, blank=True)
    order_ticket_price = models.DecimalField(max_digits=19, decimal_places=3)
    order_ticket_quantity = models.PositiveIntegerField()
    real_amount = models.DecimalField(max_digits=19, decimal_places=3)
    coupon_amount = models.DecimalField(max_digits=19, decimal_places=3)
    refund_qty = models.PositiveIntegerField()
    refund_amount = models.PositiveIntegerField()
    qty_processed = models.PositiveIntegerField(default=0)
    amount_rocessed = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
