from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RestaurantManager(models.Manager):
    """Prefetches info about visits for selected restaurant."""

    def get_queryset(self):
        return super().get_queryset().prefetch_related("visits")


class Restaurant(models.Model):
    name = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    cuisine = models.CharField(max_length=128)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
    visited_objects = RestaurantManager()

    @property
    def average_rating(self):
        avr_rating = self.visits.aggregate(models.Avg("rating"))["rating__avg"]
        if avr_rating is None:
            return 0.0
        return avr_rating

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        unique_together = [["creator", "name"]]


class Visit(models.Model):
    date = models.DateField(default=date.today)
    bill = models.PositiveIntegerField()
    notes = models.TextField(max_length=511, blank=True)
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="visits")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str__(self):
        return self.date

    class Meta:
        ordering = ["-date"]
