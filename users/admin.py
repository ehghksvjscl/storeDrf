"""
Django admin 커스터마이징
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from users import models

admin.site.register(models.User)