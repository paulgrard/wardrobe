from django.contrib import admin
from dressingManage.models import Category, Clothe, Color, Theme, Pattern, Quantity, Outfit
from userManage.models import Parameters

# Register your models here.


class ThemeAdmin(admin.ModelAdmin):
    list_display   = ('name', 'id', 'userOwner')
    list_filter    = ('name',)
    search_fields  = ('name', 'id', 'userOwner')

class ClotheAdmin(admin.ModelAdmin):
    list_display   = ('id', 'photo', 'user')
    list_filter    = ('user',)
    search_fields  = ('id', 'photo', 'user')

class CategoryAdmin(admin.ModelAdmin):
    list_display   = ('name', 'layer', 'warmth', 'area', 'id')
    list_filter    = ('id',)
    search_fields  = ('name', 'layer', 'id', 'warmth', 'area')

class ColorAdmin(admin.ModelAdmin):
    list_display   = ('name', 'id')
    list_filter    = ('id',)
    search_fields  = ('name', 'id')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Clothe, ClotheAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Quantity)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Pattern)
admin.site.register(Parameters)
admin.site.register(Outfit)
