from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

@python_2_unicode_compatible
class Order(models.Model):
    problem = models.CharField(max_length=30)
    telephone = models.CharField(max_length = 10)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.telephone

@python_2_unicode_compatible
class Comment(models.Model):
    order_info = models.ForeignKey(Order)
    comment_text = models.CharField(max_length = 30)

    def __str__(self):
        return self.comment_text

