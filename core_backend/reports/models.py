from django.db import models
from django.contrib.auth.models import User

class CitizenProfile(models.Model):
    """
    Extends the built-in Django User model to store additional 
    registration data (Phone, Age, Pincode, City) securely.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField()
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.city}"


class Incident(models.Model):
    """
    Stores the civic issues reported by citizens. 
    Enhanced with User permissions, Status tracking, and Dashboard metrics.
    """
    STATUS_CHOICES = [
        ('Pending', 'Under Processing'),
        ('Resolved', 'Solution Provided'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')

    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    location_name = models.CharField(max_length=255, blank=True)
    location_city = models.CharField(max_length=100, blank=True, help_text="Used for Dashboard (e.g., Varanasi 221001)")

    department = models.CharField(max_length=255, blank=True)
    authority_email = models.EmailField(blank=True, null=True)
    drafted_letter = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    date_filed = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_filed'] 

    def __str__(self):
        return f"REQ-{self.id} | {self.department} ({self.status})"