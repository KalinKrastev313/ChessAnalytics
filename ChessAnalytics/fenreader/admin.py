from django.contrib import admin

from ChessAnalytics.fenreader.models import FenPosition, PGN


class FenPositionAdmin(admin.ModelAdmin):
    list_display = ('fen', 'is_a_puzzle',)


class PGNAdmin(admin.ModelAdmin):
    list_display = ('pgn_moves',)


admin.site.register(FenPosition, FenPositionAdmin)
admin.site.register(PGN, PGNAdmin)
