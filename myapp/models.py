from django.db import models


class Link(models.Model):
    """
    Django model.
    Details one link scraped from a website.
    """

    def __str__(self):
        return self.name

    address = models.CharField(max_length=1000, null=True)
    name = models.CharField(max_length=1000, null=True)
