from django.db import models
from django.conf import settings


class Referal(models.Model):
    own = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referals"
    )
    follow = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed",
    )

    def __str__(self):
        return f"{self.own} - {self.follow}"

    class Meta:
        verbose_name = "Referal"
        verbose_name_plural = "Referals"
