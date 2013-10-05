from django.db import models


class NotificationOK(models.Model):
    id = models.IntegerField
    notification_number = models.CharField(max_length=19)
    create_date = models.DateTimeField()
    publish_date = models.DateTimeField()
    order_name = models.CharField(max_length=200)
    href = models.CharField(max_length=200)
    reg_num = models.IntegerField()
    max_price = models.FloatField()

