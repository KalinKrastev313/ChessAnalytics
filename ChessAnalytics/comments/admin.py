from django.contrib import admin

from ChessAnalytics.comments.models import FenComment


class FenCommentAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'to_position', 'content', 'date_time_of_publication', )
    ordering = ('-date_time_of_publication', )
    search_fields = ('content',)


admin.site.register(FenComment, FenCommentAdmin)
