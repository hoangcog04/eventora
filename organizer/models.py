from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
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
    summary = models.TextField()
    host_name = models.CharField(max_length=255)
    sorting = models.FloatField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Attribute(models.Model):
    SELECT_TYPE_CHOICES = [(0, "No Selection"), (1, "Single"), (2, "Multiple")]
    INPUT_TYPE_CHOICES = [(0, "No Entry"), (1, "Manual"), (2, "Select From List")]
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
    value = models.TextField()


class CheckoutSetting(models.Model):
    CHECKOUT_METHOD = [(0, "Default"), (1, "Offline"), (2, "Payment system")]
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    country_code = models.CharField(max_length=3)
    currency_code = models.CharField(max_length=3)
    checkout_method = models.PositiveSmallIntegerField(
        choices=CHECKOUT_METHOD, default=0
    )
    offline_note = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)


class Coupon(models.Model):
    USE_TYPE = [(0, "Amount off"), (1, "Percent off")]
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
    ticket_ids = models.TextField()


class CouponHistory(models.Model):
    USE_TYPE = [(0, "Amount off"), (1, "Percent off")]
    id = models.BigAutoField(primary_key=True)
    coupon_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    order_id = models.ForeignKey(Dummy2, null=True, on_delete=models.SET_NULL)
    coupon_code = models.CharField(max_length=255)
    redeemer_name = models.CharField(max_length=255)
    order_sn = models.CharField(max_length=255, null=True)
    use_time = models.DateTimeField(auto_now_add=True)


class Event(models.Model):
    STATUS = [(0, "Draft"), (1, "Live"), (2, "Started"), (3, "Ended"), (4, "Canceled")]
    IS_FREE = [(0, "No"), (1, "Yes")]
    id = models.BigAutoField(primary_key=True)
    organizer_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    venue_id = models.ForeignKey(Dummy1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    pic = models.TextField()
    album_pics = models.TextField()
    date = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    capacity = models.PositiveIntegerField()
    is_free = models.PositiveSmallIntegerField(choices=IS_FREE, default=0)
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
    IS_FREE = [(0, "No"), (1, "Yes")]
    IS_HIDDEN = [(0, "No"), (1, "Yes")]
    id = models.BigAutoField(primary_key=True)
    event_id = models.ForeignKey(Dummy, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    summary = models.TextField()
    pic = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=3)
    capacity = models.PositiveIntegerField()
    quantity_sold = models.PositiveIntegerField()
    max_quantity_per_order = models.PositiveIntegerField()
    sorting = models.FloatField()
    is_free = models.PositiveSmallIntegerField(choices=IS_FREE, default=0)
    is_hidden = models.PositiveSmallIntegerField(choices=IS_HIDDEN, default=0)
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
