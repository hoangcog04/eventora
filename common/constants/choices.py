SELECT_TYPE_CHOICES = [(0, "No Selection"), (1, "Single"), (2, "Multiple")]
INPUT_TYPE_CHOICES = [(0, "No Entry"), (1, "Manual"), (2, "Select From List")]

CHECKOUT_METHOD = [(0, "Default"), (1, "Offline"), (2, "Payment system")]

USE_TYPE = [(0, "Amount off"), (1, "Percent off")]

EVENT_STATUS = [
    (0, "Draft"),
    (1, "Live"),
    (2, "Started"),
    (3, "Ended"),
    (4, "Canceled"),
]

ORDER_STATUS = [
    (0, "Default"),
    (1, "Started"),
    (2, "Pending"),
    (3, "Completed"),
    (4, "Abandoned"),
]
DELIVERY_METHOD = [(0, "Email"), (1, "Phone")]

REFUND_REQUEST_STATUS = [
    (0, "Pending"),
    (1, "Refunding"),
    (2, "Processed"),
    (3, "Rejected"),
    (4, "Error"),
]
