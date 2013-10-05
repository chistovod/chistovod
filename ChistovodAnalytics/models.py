from django.db import models


class Lot(models.Model):
    sid = models.CharField(max_length=20)
    notification_number = models.CharField(max_length=19)
    create_date = models.DateTimeField()
    publish_date = models.DateTimeField()
    notification_name = models.CharField(max_length=200)
    lot_name = models.CharField(max_length=200)
    href = models.CharField(max_length=200)
    max_price = models.FloatField()
    reg_num = models.CharField(max_length=15)
    ordinal_number = models.IntegerField()
    final_price = models.FloatField(null=True)
    contract_sign_date = models.DateTimeField(null=True)
    execution_date = models.DateTimeField(null=True)


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

