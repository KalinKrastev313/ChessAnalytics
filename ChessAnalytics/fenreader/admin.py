from django.contrib import admin

from ChessAnalytics.fenreader.models import FenPosition, PGN


class FenPositionAdmin(admin.ModelAdmin):
    list_display = ('fen', 'is_a_puzzle',)
    ordering = ('-is_a_puzzle',)
    search_fields = ('white_player', 'black_player', )


class PGNAdmin(admin.ModelAdmin):
    list_display = ('pgn_moves',)
    list_filter = ('time_control',)


admin.site.register(FenPosition, FenPositionAdmin)
admin.site.register(PGN, PGNAdmin)
