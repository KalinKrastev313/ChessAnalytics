from django.contrib import admin

from ChessAnalytics.fenreader.models import FenPosition


class FenPositionAdmin(admin.ModelAdmin):
    list_display = ('fen', 'is_a_puzzle', 'best_lines')


admin.site.register(FenPosition, FenPositionAdmin)
