from django.contrib import admin
from dressingManage.models import Category, Clothe, Color, Theme, Pattern, Parameter

# Register your models here.


class ThemeAdmin(admin.ModelAdmin):
    list_display   = ('name', 'id', 'userOwner')
    list_filter    = ('name',)
    search_fields  = ('name', 'id', 'userOwner')

class ClotheAdmin(admin.ModelAdmin):
    list_display   = ('id', 'photo', 'user')
    list_filter    = ('user',)
    search_fields  = ('id', 'photo', 'user')
    
admin.site.register(Category)
admin.site.register(Clothe, ClotheAdmin)
admin.site.register(Color)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Pattern)
admin.site.register(Parameter)
