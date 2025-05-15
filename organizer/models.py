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
    session_name = models.CharField(max_length=100)
    summary = models.TextField()
    host_name = models.CharField(max_length=100)
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
    attribute_category_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    select_type = models.PositiveSmallIntegerField(
        choices=SELECT_TYPE_CHOICES, default=0
    )
    input_type = models.IntegerField(choices=INPUT_TYPE_CHOICES, default=0)
    input_list = models.TextField(blank=True, null=True)


class AttributeCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
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
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    use_count = models.PositiveIntegerField()
    use_type = models.PositiveSmallIntegerField(choices=USE_TYPE, default=0)
    amount_off = models.DecimalField(max_digits=19, decimal_places=3)
    percent_off = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    code = models.CharField(max_length=100)
    ticket_ids = models.TextField()
