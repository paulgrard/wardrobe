# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User



class Parameters(models.Model):
    user = models.OneToOneField(User)
    #weatherEnabled = models.BooleanField()
    #chilliness = models.PositiveIntegerField()
    sex = models.PositiveIntegerField()
            
    def __str__(self):
        return self.user.username
