

# Create your models here.
from django.db import models
class Business(models.Model):
    caption = models.CharField(max_length=32)
    code = models.IntegerField()


class Hosts(models.Model):
    hostname = models.CharField(max_length=32)
    ip = models.GenericIPAddressField(max_length=32,unique=True)
    port = models.IntegerField()
    business = models.ForeignKey(to='Business',to_field='id')

class Application(models.Model):
    name = models.CharField(max_length=32)
    r = models.ManyToManyField('Hosts')

