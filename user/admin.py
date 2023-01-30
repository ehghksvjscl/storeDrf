"""
Django admin 커스터마이징
"""

from django.contrib import admin

from user import models

admin.site.register(models.User)
