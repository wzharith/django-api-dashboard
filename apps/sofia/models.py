from django.db import models

# Create your models here.

class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    paid_amount = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(auto_now_add=True) #blank=True, null=True

    def __str__(self):
        return '%s' % self.name