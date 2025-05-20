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
from common.constants.countries import GET_COUNTRIES, GET_CURRENCIES


class Venue(models.Model):
    id = models.BigAutoField(primary_key=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=255)
    city = models.TextField()
    country = models.TextField()
    detail_address = models.TextField(blank=True)
    google_place_id = models.TextField(blank=True)
    latiude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        validators=[
            MinValueValidator(Decimal("-90.0")),
            MaxValueValidator(Decimal("90.0")),
        ],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        validators=[
            MinValueValidator(Decimal("-180.0")),
            MaxValueValidator(Decimal("180.0")),
        ],
    )


class AttributeCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    attribute_count = models.PositiveSmallIntegerField(null=True)


class Attribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    attribute_category = models.ForeignKey(
        AttributeCategory, null=True, on_delete=models.SET_NULL
    )
    attribute_category_name = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    select_type = models.PositiveSmallIntegerField(
        choices=SelectType.choices, default=SelectType.NO_SELECTION
    )
    input_type = models.IntegerField(
        choices=InputType.choices, default=InputType.NO_ENTRY
    )
    input_list = models.TextField(blank=True)


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    venue = models.ForeignKey(Venue, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    pic = models.TextField(blank=True)
    album_pics = models.TextField(blank=True)
    date = models.DateTimeField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    status = models.PositiveSmallIntegerField(
        choices=EventStatus.choices, default=EventStatus.DRAFT
    )
    capacity = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
    publish_time = models.DateTimeField(null=True)


class Coupon(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    use_count = models.PositiveIntegerField(default=0)
    use_type = models.PositiveSmallIntegerField(
        choices=UseType.choices, default=UseType.AMOUNT_OFF
    )
    amount_off = models.DecimalField(max_digits=19, decimal_places=3, null=True)
    percent_off = models.PositiveSmallIntegerField(null=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    code = models.CharField(max_length=255)
    ticket_ids = models.TextField(blank=True)


class CouponHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    coupon = models.ForeignKey(Coupon, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )
    order = models.ForeignKey("hub.Order", null=True, on_delete=models.SET_NULL)
    coupon_code = models.CharField(max_length=255)
    redeemer_name = models.CharField(max_length=255, blank=True)
    order_sn = models.CharField(max_length=255, blank=True)
    use_time = models.DateTimeField(auto_now_add=True)


class CheckoutSetting(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    country_code = models.CharField(choices=GET_COUNTRIES, max_length=3, blank=True)
    currency_code = models.CharField(choices=GET_CURRENCIES, max_length=3, blank=True)
    checkout_method = models.PositiveSmallIntegerField(
        choices=CheckoutMethod.choices, default=CheckoutMethod.DEFAULT
    )
    offline_note = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class AttributeValue(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    attribute_category = models.ForeignKey(
        AttributeCategory, null=True, on_delete=models.SET_NULL
    )
    attribute = models.ForeignKey(Attribute, null=True, on_delete=models.SET_NULL)
    value = models.TextField(blank=True)


class Agenda(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    session_name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    host_name = models.CharField(max_length=255)
    sorting = models.FloatField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Faq(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    question = models.TextField()
    answer = models.TextField()
    sorting = models.FloatField(null=True)


class Ticket(models.Model):
    id = models.BigAutoField(primary_key=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    pic = models.TextField(blank=True)
    price = models.DecimalField(max_digits=19, decimal_places=3)
    capacity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField(default=0)
    max_quantity_per_order = models.PositiveIntegerField(default=10)
    sorting = models.FloatField(null=True)
    is_free = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class TicketStock(models.Model):
    id = models.BigAutoField(primary_key=True)
    ticket = models.ForeignKey(Ticket, null=True, on_delete=models.SET_NULL)
    quantity_available = models.PositiveIntegerField(null=True)
    quantity_lock = models.PositiveIntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)
