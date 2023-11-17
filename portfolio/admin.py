from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Portfolio, CUser, College, Major, Number

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'content']

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(CUser, UserAdmin)

class CollegeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(College, CollegeAdmin)

class MajorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

admin.site.register(Major, MajorAdmin)

admin.site.register(Number)
