# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)
    warmth = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)], blank = True, null = True)
    area = models.PositiveIntegerField()
    layer = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(3)], null = True)
    def __str__(self):
        return str(self.name)
    

class Clothe(models.Model):
    warmth = models.PositiveIntegerField()
    photo = models.CharField(max_length=30, null=True)
    state = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(2)])
    nbreUse = models.PositiveIntegerField()
    category = models.ForeignKey('Category')
    themes = models.ManyToManyField('Theme')
    user = models.ForeignKey(User)
    colors = models.ManyToManyField('Color')
    quantities = models.ManyToManyField('Quantity')
    
    def __str__(self):
        return self.photo

class Quantity(models.Model):
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    color = models.ForeignKey('Color')

    def __str__(self):
        return str(self.quantity)
    
class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Theme(models.Model):
    name = models.CharField(max_length=30)
    userOwner = models.ForeignKey(User, blank = True, null = True)
    
    def __str__(self):
        return self.name


class Pattern(models.Model):
    name = models.CharField(max_length=30)
    colors = models.ManyToManyField(Color)
        
    def __str__(self):
        return self.name

class Outfit(models.Model):
    firstLayer = models.OneToOneField(Clothe, related_name="firstLayer_outfit", null = True)
    secondLayer = models.OneToOneField(Clothe, related_name="secondLayer_outfit", null = True)
    pant = models.OneToOneField(Clothe, related_name="pant_outfit", null = True)
    shoes = models.OneToOneField(Clothe, related_name="shoes_outfit", null = True)
    coat = models.OneToOneField(Clothe, related_name="coat_outfit", null = True)
    underwear = models.OneToOneField(Clothe, related_name="underwear_outfit", null = True)
    underwearTop = models.OneToOneField(Clothe, related_name="underwearTop_outfit", null = True)
    sock = models.OneToOneField(Clothe, related_name="sock", null = True)

    various = models.ManyToManyField(Clothe, blank = True)
    userOwner = models.OneToOneField(User, null = True)
    generating = models.NullBooleanField()
    nbrLayer = models.PositiveIntegerField(null = True)
    #temp = models.PositiveIntegerField(null = True)
    weather = models.CharField(max_length=30, null = True)
    ptsTop = models.PositiveIntegerField(null = True)
    ptsPant = models.PositiveIntegerField(null = True)
    ptsCoat = models.PositiveIntegerField(null = True)
    ptsShoes = models.PositiveIntegerField(null = True)
    ptsVarious = models.PositiveIntegerField(null = True)
    theme = models.OneToOneField(Theme, null = True)

    def __str__(self):
        return self.userOwner.username
