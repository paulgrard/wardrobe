from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

# Create your models here.                      pas d'ajout pattern et pas d'ajout de categorie

class Category(models.Model):
    name = models.CharField(max_length=30)   # passer en int?    old = max_length=30
    warmth = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)], blank = True, null = True)
    area = models.PositiveIntegerField()
    def __str__(self):
        return str(self.name)

'''class Area(models.Model):
    area = models.CharField(max_length=30)
    #categ = models.ForeignKey('Categorie')
    def __str__(self):
        return self.area'''
    
# mettre une limite pour warmth
class Clothe(models.Model):
    warmth = models.PositiveIntegerField()
    photo = models.CharField(max_length=30)
    state = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(2)])
    nbreUse = models.PositiveIntegerField()
    category = models.ForeignKey('Category')
    themes = models.ManyToManyField('Theme', blank=True)
    user = models.ForeignKey(User)
    colors = models.ManyToManyField('Color')#models.ManyToManyField('Color')
    quantities = models.ManyToManyField('Quantity')
   # pattern = models.OneToManyField('Pattern')

    '''pour limiter les patterns a 3 ne pas oublier une methode du genre:
    def add_pattern(self, pattern):
    if self.pattern_set.count() >= 3:
         raise Exception("Trop de pattern !!")

    self.pattern_set.add(player)'''
    
    def __str__(self):
        return self.photo

class Quantity(models.Model):
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    color = models.ForeignKey('Color') #OneToOneField('Color')

    def __str__(self):
        return str(self.quantity)
    
class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Theme(models.Model):
    name = models.CharField(max_length=30)
    userOwner = models.ForeignKey(User)
    
    def __str__(self):
        return self.name


class Pattern(models.Model):   #lier to color              +       couleur joker       + champs bool joker
    name = models.CharField(max_length=30)
    #clothe = models.ForeignKey(Clothes)
    ''' on y accède avec un Clothes object c comme ça :
    c.pattern_set.objects.all() '''
    color = models.ManyToManyField(Color)
    #jokerEnabled = models.BooleanField()
    #jokerColor = models.CharField(max_length=7)
        
    def __str__(self):
        return self.name

class Parameter(models.Model):
    user = models.OneToOneField(User)
    weatherEnabled = models.BooleanField()
    chilliness = models.PositiveIntegerField()
            
    def __str__(self):
        return self.user.username
