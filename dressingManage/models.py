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
    color = models.ManyToManyField(Color)
        
    def __str__(self):
        return self.name

class Outfit(models.Model):
    clothes = models.ForeignKey(Clothe, blank = True, null = True)
    wearing = models.NullBooleanField()

    def __str__(self):
        return self.clothes

class outfitStorage(models.Model):
    clothes = models.ForeignKey(Clothe, blank = True, null = True)
    userOwner = models.OneToOneField(User, blank = True, null = True)

    def __str__(self):
        return self.userOwner.name
