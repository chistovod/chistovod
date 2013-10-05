from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    
class NotificationOK(models.Model):
    id = models.IntegerField
    notification_number = models.CharField(max_length=19)
    create_date
    publish_date
    order_name
    href
    reg_num
    max_price

