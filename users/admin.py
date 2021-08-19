from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.conf import settings

from .models import Favorites
class FavoritesInline(admin.StackedInline):
    model = Favorites
    can_delete = False
    verbose_name_plural = 'favorites'

class UserAdmin(BaseUserAdmin):
    inlines = (FavoritesInline)


admin.site.unregister(settings.AUTH_USER_MODEL)
admin.site.register(settings.AUTH_USER_MODEL, UserAdmin)
