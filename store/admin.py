"""
Django admin 커스터마이징
"""

from django.contrib import admin

from store import models

admin.site.register(models.Product)
admin.site.register(models.Option)
admin.site.register(models.Cart)
admin.site.register(models.Order)