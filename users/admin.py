from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

from .models import Favorites, Team
class FavoritesInline(admin.StackedInline):
    model = Favorites
    can_delete = False
    verbose_name_plural = 'favorites'

class UserAdmin(BaseUserAdmin):
    inlines = (FavoritesInline,)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(Favorites)