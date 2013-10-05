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


class Customer(models.Model):
    registration_number = models.BigIntegerField()
    inn = models.BigIntegerField()
    okato = models.IntegerField()
    name = models.CharField(max_length=200)


class Supplier(models.Model):
    inn = models.CharField(max_length=100)
    participant_type = models.CharField(max_length=100)
    organization_form = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=100)


class Contact(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)

