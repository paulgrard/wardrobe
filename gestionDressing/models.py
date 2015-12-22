from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.                      pas d'ajout pattern et pas d'ajout de categorie

class Categories(models.Model):
    name = models.CharField(max_length=30)
    warmth = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(3)])
    area = models.CharField(max_length=30)  #table a part mais tjrs char
    
    def __str__(self):
        return self.name


class Clothes(models.Model):
    color = models.CharField(max_length=7) #table a part
    warmth = models.PositiveIntegerField()
    photo = models.ImageField()
    state = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(2)])
    nbreUse = models.PositiveIntegerField()
    categorie = models.ForeignKey('Categories')
    theme = models.ManyToManyField('Themes')
   # pattern = models.OneToManyField('Pattern')

    '''pour limiter les patterns a 3 ne pas oublier une methode du genre:
    def add_pattern(self, pattern):
    if self.pattern_set.count() >= 3:
         raise Exception("Trop de pattern !!")

    self.pattern_set.add(player)'''
    
    def __str__(self):
        return self.photo


class Themes(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name


class Pattern(models.Model):   #lier to color              +       couleur joker       + champs bool joker
    name = models.CharField(max_length=30)
    clothe = models.ForeignKey(Clothes)
    ''' on y accède avec un Clothes object c comme ça :
    c.pattern_set.objects.all() '''
    
    def __str__(self):
        return self.name
