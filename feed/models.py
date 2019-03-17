from django.db import models


class Offer(models.Model):
    """
    backbone for Offer model (Arina, napishi model ples)
    """
    title = models.CharField(max_length=250)

