from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.constants.choices import (
    CheckoutMethod,
    EventStatus,
    InputType,
    SelectType,
    UseType,
)
from common.constants.code import GET_COUNTRIES, GET_CURRENCIES


class Venue(models.Model):
    id = models.BigAutoField(primary_key=True)
    organizer_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
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


class AttributeCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    attribute_count = models.PositiveSmallIntegerField()


class Attribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute_category_id = models.ForeignKey(
        AttributeCategory, null=True, on_delete=models.SET_NULL
    )
    attribute_category_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    select_type = models.PositiveSmallIntegerField(
        choices=SelectType.choices, default=SelectType.NO_SELECTION
    )
    input_type = models.IntegerField(
        choices=InputType.choices, default=InputType.NO_ENTRY
    )
    input_list = models.TextField(blank=True, null=True)


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    organizer_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    venue_id = models.ForeignKey(Venue, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    pic = models.TextField(blank=True)
    album_pics = models.TextField(blank=True)
    date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.PositiveSmallIntegerField(
        choices=EventStatus.choices, default=EventStatus.DRAFT
    )
    capacity = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    publish_time = models.DateTimeField()


class Coupon(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    use_count = models.PositiveIntegerField()
    use_type = models.PositiveSmallIntegerField(
        choices=UseType.choices, default=UseType.AMOUNT_OFF
    )
    amount_off = models.DecimalField(null=True, max_digits=19, decimal_places=3)
    percent_off = models.PositiveSmallIntegerField(null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    code = models.CharField(max_length=255)
    ticket_ids = models.TextField(blank=True)


class CouponHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    coupon_id = models.ForeignKey(Coupon, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    order_id = models.ForeignKey("hub.Order", null=True, on_delete=models.SET_NULL)
    coupon_code = models.CharField(max_length=255)
    redeemer_name = models.CharField(max_length=255)
    order_sn = models.CharField(max_length=255, null=True)
    use_time = models.DateTimeField(auto_now_add=True)


class CheckoutSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    country_code = models.CharField(choices=GET_COUNTRIES, max_length=3)
    currency_code = models.CharField(choices=GET_CURRENCIES, max_length=3)
    checkout_method = models.PositiveSmallIntegerField(
        choices=CheckoutMethod.choices, default=CheckoutMethod.DEFAULT
    )
    offline_note = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class AttributeValue(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    attribute_category_id = models.ForeignKey(
        AttributeCategory, null=True, on_delete=models.SET_NULL
    )
    attribute_id = models.ForeignKey(Attribute, null=True, on_delete=models.SET_NULL)
    value = models.TextField(blank=True)


class Agenda(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    session_name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    host_name = models.CharField(max_length=255)
    sorting = models.FloatField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Faq(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    question = models.TextField()
    answer = models.TextField()
    sorting = models.FloatField()


class Ticket(models.Model):
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
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
    ticket_id = models.ForeignKey(Ticket, null=True, on_delete=models.SET_NULL)
    quantity_available = models.PositiveIntegerField()
    quantity_lock = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
