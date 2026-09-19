from django.db import models

class Incident(models.Model):
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    drafted_letter = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location_name} - {self.department}"