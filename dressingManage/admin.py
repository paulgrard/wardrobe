from django.contrib import admin
from dressingManage.models import Category, Clothe, Color, Theme, Pattern, Parameter

# Register your models here.


class ThemeAdmin(admin.ModelAdmin):
    list_display   = ('name', 'id', 'userOwner')
    list_filter    = ('name',)
    search_fields  = ('name', 'id', 'userOwner')

    
admin.site.register(Category)
admin.site.register(Clothe)
admin.site.register(Color)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Pattern)
admin.site.register(Parameter)
