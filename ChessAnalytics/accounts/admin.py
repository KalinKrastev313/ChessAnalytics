from django.contrib import admin
from django.contrib.auth.models import User, Group

from ChessAnalytics.accounts.models import ChessAnalyticsUser


class ChessAnalyticsUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'rating', 'is_superuser',)


admin.site.register(ChessAnalyticsUser, ChessAnalyticsUserAdmin)


def is_teacher(user):
    if user.groups.filter(name='Teacher').exists():
        return True
    else:
        return False


def is_student(user):
    return user.groups.filter(name='Student').exists()

