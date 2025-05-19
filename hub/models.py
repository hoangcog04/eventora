from django.db import models

from common.constants.choices import (
    CHECKOUT_METHOD,
    DELIVERY_METHOD,
    ORDER_STATUS,
    REFUND_REQUEST_STATUS,
)


class Dummy(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False


class Dummy1(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False


class Dummy2(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    event_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    coupon_id = models.ForeignKey(Dummy2, null=True, on_delete=models.SET_NULL)
    order_sn = models.CharField(max_length=255, null=True)
    owner_name = models.CharField(max_length=255, null=True)
    total_amount = models.DecimalField(max_digits=19, decimal_places=3)
    pay_amount = models.DecimalField(max_digits=19, decimal_places=3)
    coupon_amount = models.DecimalField(max_digits=19, decimal_places=3)
    checkout_method = models.PositiveSmallIntegerField(
        choices=CHECKOUT_METHOD, default=0
    )
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUS, default=1)
    delivery_method = models.PositiveSmallIntegerField(
        choices=DELIVERY_METHOD, default=0
    )
    receiver_name = models.CharField(max_length=255, null=True)
    payment_time = models.DateTimeField()
    delivery_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class OrderAttendee(models.Model):
    DELIVERY_METHOD = [(0, "Email"), (1, "Phone")]
    id = models.BigAutoField(primary_key=True)
    order_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    ticket_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    ticket_stock_id = models.ForeignKey(Dummy2, null=True, on_delete=models.SET_NULL)
    order_sn = models.CharField(max_length=255, null=True)
    ticket_name = models.CharField(max_length=255, null=True)
    ticket_pic = models.TextField(blank=True)
    ticket_price = models.DecimalField(max_digits=19, decimal_places=3)
    ticket_quantity = models.PositiveIntegerField()
    real_amount = models.DecimalField(max_digits=19, decimal_places=3)
    coupon_amount = models.DecimalField(max_digits=19, decimal_places=3)
    bill_receiver_email = models.CharField(max_length=255, null=True)
    receiver_email = models.CharField(max_length=255, null=True)
    refuned = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    ticket_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    order_sn = models.CharField(max_length=255, null=True)
    ticket_name = models.CharField(max_length=255, null=True)
    ticket_pic = models.TextField(blank=True)
    ticket_price = models.DecimalField(max_digits=19, decimal_places=3)
    ticket_quantity = models.PositiveIntegerField()
    real_amount = models.DecimalField(max_digits=19, decimal_places=3)
    coupon_amount = models.DecimalField(max_digits=19, decimal_places=3)


class RefundItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    refund_request_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    ticket_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    ticket_name = models.CharField(max_length=255, null=True)
    order_ticket_price = models.DecimalField(max_digits=19, decimal_places=3)
    order_ticket_quantity = models.PositiveIntegerField()
    real_amount = models.DecimalField(max_digits=19, decimal_places=3)
    coupon_amount = models.DecimalField(max_digits=19, decimal_places=3)
    refundQty = models.PositiveIntegerField()
    refundAmount = models.PositiveIntegerField()
    qty_processed = models.PositiveIntegerField()
    amount_rocessed = models.PositiveIntegerField()
    bill_receiver_email = models.CharField(max_length=255, null=True)
    receiver_email = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class RefundRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    event_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(Dummy2, null=True, on_delete=models.SET_NULL)
    order_sn = models.CharField(max_length=255, null=True)
    from_name = models.CharField(max_length=255, null=True)
    from_email = models.CharField(max_length=255, null=True)
    message = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    order_pay_amount = models.DecimalField(max_digits=19, decimal_places=3)
    checkout_method = models.PositiveSmallIntegerField(
        choices=CHECKOUT_METHOD, default=0
    )
    delivery_method = models.PositiveSmallIntegerField(
        choices=DELIVERY_METHOD, default=0
    )
    status = models.PositiveSmallIntegerField(choices=REFUND_REQUEST_STATUS, default=0)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
