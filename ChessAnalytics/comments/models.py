from django.db import models

from ChessAnalytics.accounts.models import ChessAnalyticsUser
from ChessAnalytics.fenreader.models import FenPosition


class FenComment(models.Model):
    to_user = models.ForeignKey(ChessAnalyticsUser, on_delete=models.CASCADE)
    to_position = models.ForeignKey(FenPosition, on_delete=models.CASCADE)
    content = models.CharField(blank=False, max_length=300)
    date_time_of_publication = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_time_of_publication']

