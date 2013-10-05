from django.db import models


class NotificationOK(models.Model):
    notification_id = models.IntegerField()
    notification_number = models.CharField(max_length=19)
    create_date = models.DateTimeField()
    publish_date = models.DateTimeField()
    order_name = models.CharField(max_length=200)
    href = models.CharField(max_length=200)
    reg_num = models.IntegerField()
    max_price = models.FloatField()


class Supplier(models.Model):
    inn = models.CharField()
    participant_type = models.CharField()
    organization_form = models.CharField()
    organization_name = models.CharField()


class Contract(models.Model):
    last_name = models.CharField()
    first_name = models.CharField()
    middle_name = models.CharField()

    email = models.CharField()
    phone = models.CharField()
    fax = models.CharField()
    status = models.CharField()
