from django.db import models


class SelectType(models.IntegerChoices):
    NO_SELECTION = 0, "No selection"
    SINGLE = 1, "Single"
    MULTIPLE = 2, "Multiple"


class InputType(models.IntegerChoices):
    NO_ENTRY = 0, "No entry"
    MANUAL = 1, "Manual"
    SELECT_FROM_LIST = 2, "Select from list"


class CheckoutMethod(models.IntegerChoices):
    DEFAULT = 0, "Default"
    OFFLINE = 1, "Offline"
    PAYMENT_SYSTEM = 2, "Payment system"


class UseType(models.IntegerChoices):
    AMOUNT_OFF = 0, "Amount off"
    PERCENT_OFF = 1, "Percent off"


class EventStatus(models.IntegerChoices):
    DRAFT = 0, "Draft"
    LIVE = 1, "Live"
    STARTED = 2, "Started"
    ENDED = 3, "Ended"
    CANCELED = 4, "Canceled"


class OrderStatus(models.IntegerChoices):
    DEFAULT = 0, "Default"
    STARTED = 1, "Started"
    PENDING = 2, "Pending"
    COMPLETED = 3, "Completed"
    ABANDONED = 4, "Abandoned"


class DeliveryMethod(models.IntegerChoices):
    EMAIL = 0, "Email"
    PHONE = 1, "Phone"


class RefundRequestStatus(models.IntegerChoices):
    PENDING = 0, "Pending"
    REFUNDING = 1, "Refunding"
    PROCESSED = 2, "Processed"
    REJECTED = 3, "Rejected"
    ERROR = 4, "Error"
