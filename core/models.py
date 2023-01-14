from django.db import models

# Create your models here.


class AccessControl(models.Model)  :
    username = models.CharField(max_length=40)
    trials = models.PositiveIntegerField(null = False,default=1)  #defaults to 1 on creation