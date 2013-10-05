from django.db import models


class Lot(models.Model):
    notification_number = models.CharField(max_length=19, db_index=True)
    create_date = models.DateTimeField(db_index=True)
    publish_date = models.DateTimeField(db_index=True)
    notification_name = models.CharField(max_length=200)
    lot_name = models.CharField(max_length=200)
    href = models.CharField(max_length=200)
    max_price = models.FloatField(db_index=True)
    registration_number = models.BigIntegerField(db_index=True)
    ordinal_number = models.IntegerField(db_index=True)
    final_price = models.FloatField(null=True, db_index=True)
    contract_sign_date = models.DateTimeField(null=True, db_index=True)
    execution_date = models.DateTimeField(null=True, db_index=True)


class Customer(models.Model):
    registration_number = models.BigIntegerField(db_index=True)
    inn = models.BigIntegerField(db_index=True)
    okato = models.IntegerField(db_index=True)
    name = models.CharField(max_length=200)


class Supplier(models.Model):
    inn = models.CharField(max_length=100, db_index=True)
    participant_type = models.CharField(max_length=100)
    organization_form = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=200)


class Contact(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    fax = models.CharField(max_length=50)

