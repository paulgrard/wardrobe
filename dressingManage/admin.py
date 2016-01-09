from django.contrib import admin
from dressingManage.models import Category, Clothe, Color, Theme, Pattern, Parameter

# Register your models here.

admin.site.register(Category)
admin.site.register(Clothe)
admin.site.register(Color)
admin.site.register(Theme)
admin.site.register(Pattern)
admin.site.register(Parameter)
