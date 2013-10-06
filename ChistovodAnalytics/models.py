from django.db import models


class Organization(models.Model):
    inn = models.BigIntegerField(db_index=True, primary_key=True)
    name = models.CharField(max_length=200)


class Customer(Organization):
    registration_number = models.BigIntegerField(db_index=True)
    okato = models.IntegerField(db_index=True)


class Supplier(Organization):
    participant_type = models.CharField(max_length=100)
    organization_form = models.CharField(max_length=100)


class Lot(models.Model):
    notification_number = models.CharField(max_length=19, db_index=True)
    create_date = models.DateTimeField(db_index=True)
    publish_date = models.DateTimeField(db_index=True)
    notification_name = models.CharField(max_length=200)
    lot_name = models.CharField(max_length=200)
    href = models.CharField(max_length=200)
    max_price = models.FloatField(db_index=True)
    ordinal_number = models.IntegerField(db_index=True)
    final_price = models.FloatField(null=True, db_index=True)
    contract_sign_date = models.DateTimeField(null=True, db_index=True)
    execution_date = models.DateTimeField(null=True, db_index=True)

    customer_set = models.ManyToManyField(Customer, through='LotCustomer')
    supplier_set = models.ManyToManyField(Supplier, through='LotSupplier')


class LotCustomer(models.Model):
    lot_id = models.ForeignKey(Lot)
    customer_inn = models.ForeignKey(Customer)
    is_initiator = models.BooleanField(db_index=True)


class LotSupplier(models.Model):
    lot_id = models.ForeignKey(Lot)
    supplier_inn = models.ForeignKey(Supplier)
    is_winner = models.BooleanField(db_index=True)


class Contact(models.Model):
    inn = models.ForeignKey(Organization)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=50, null=True)
    fax = models.CharField(max_length=50, null=True)


class Contract(models.Model):
    notification_number = models.CharField(max_length=20)
    lot_number = models.IntegerField()
    sign_date = models.DateTimeField()
    price = models.FloatField()
    current_contract_stage = models.CharField(max_length=10)
    execution = models.CharField(max_length=10)
