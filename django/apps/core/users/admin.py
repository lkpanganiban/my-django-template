from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile, Subscriptions


# Register your models here.
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


class SubscriptionsInline(admin.StackedInline):
    model = Subscriptions
    can_delete = False
    verbose_name_plural = "Subscriptions"


class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    inlines = (
        ProfileInline,
        SubscriptionsInline,
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "login_count",
        "account_expiry",
        "is_active",
    )
    list_filter = ("user__is_active",)

    @staticmethod
    def is_active(obj):
        return obj.user.is_active


class SubscriptionsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Subscriptions, SubscriptionsAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
