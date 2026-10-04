from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class Country(models.Model):
    name=models.CharField(max_length=100)

    def str(self):
        return self.name

class CustomUser(AbstractUser):
    avatar =models.ImageField(upload_to='avatar/',null=True,blank=True)
    id_country = models.ForeignKey(Country,on_delete=models.SET_NULL,null=True,blank=True)
    phone = models.CharField(max_length=20,blank=True,null=True)
    city = models.CharField(max_length=100,blank=True,null=True)