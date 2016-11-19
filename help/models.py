from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
import datetime

class Order(models.Model):
    
    address = models.CharField(max_length = 20)
    problem = models.CharField(max_length=30)
    telephone = models.CharField(max_length = 10)    
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.telephone

class Comment(models.Model):

    order_info = models.ForeignKey(Order)
    comment_text = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.comment_text
