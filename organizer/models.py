from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.constants.choices import (
    CHECKOUT_METHOD,
    EVENT_STATUS,
    INPUT_TYPE_CHOICES,
    SELECT_TYPE_CHOICES,
    USE_TYPE,
)
from common.constants.code import GET_COUNTRIES, GET_CURRENCIES


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


class Agenda(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    session_name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    host_name = models.CharField(max_length=255)
    sorting = models.FloatField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Attribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute_category_id = models.ForeignKey(
        Dummy, null=True, on_delete=models.SET_NULL
    )
    attribute_category_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    select_type = models.PositiveSmallIntegerField(
        choices=SELECT_TYPE_CHOICES, default=0
    )
    input_type = models.IntegerField(choices=INPUT_TYPE_CHOICES, default=0)
    input_list = models.TextField(blank=True, null=True)


class AttributeCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    attribute_count = models.PositiveSmallIntegerField()


class AttributeValue(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    attribute_category_id = models.ForeignKey(
        Dummy1, null=True, on_delete=models.SET_NULL
    )
    attribute_id = models.ForeignKey(Dummy2, null=True, on_delete=models.SET_NULL)
    value = models.TextField(blank=True)


class CheckoutSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    country_code = models.CharField(choices=GET_COUNTRIES, max_length=3)
    currency_code = models.CharField(choices=GET_CURRENCIES, max_length=3)
    checkout_method = models.PositiveSmallIntegerField(
        choices=CHECKOUT_METHOD, default=0
    )
    offline_note = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Coupon(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    use_count = models.PositiveIntegerField()
    use_type = models.PositiveSmallIntegerField(choices=USE_TYPE, default=0)
    amount_off = models.DecimalField(max_digits=19, decimal_places=3)
    percent_off = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    code = models.CharField(max_length=255)
    ticket_ids = models.TextField(blank=True)


class CouponHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    coupon_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    order_id = models.ForeignKey(Dummy2, null=True, on_delete=models.SET_NULL)
    coupon_code = models.CharField(max_length=255)
    redeemer_name = models.CharField(max_length=255)
    order_sn = models.CharField(max_length=255, null=True)
    use_time = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    organizer_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    venue_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    pic = models.TextField(blank=True)
    album_pics = models.TextField(blank=True)
    date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.PositiveSmallIntegerField(choices=EVENT_STATUS, default=0)
    capacity = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    publish_time = models.DateTimeField()


class Faq(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    question = models.TextField()
    answer = models.TextField()
    sorting = models.FloatField()


class Ticket(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    pic = models.TextField(blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=3)
    capacity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField()
    max_quantity_per_order = models.PositiveIntegerField()
    sorting = models.FloatField()
    is_free = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class TicketStock(models.Model):
    id = models.BigAutoField(primary_key=True)
    ticket_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    quantity_available = models.PositiveIntegerField()
    quantity_lock = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Venue(models.Model):
    id = models.BigAutoField(primary_key=True)
    organizer_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    city = models.TextField()
    country = models.TextField()
    detail_address = models.TextField()
    google_place_id = models.TextField()
    latiude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(Decimal("-90.0")),
            MaxValueValidator(Decimal("90.0")),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(Decimal("-180.0")),
            MaxValueValidator(Decimal("180.0")),
        ],
    )
