from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    INTEREST_CHOICES = [
        ('Planting', 'Tree Planting & Greening'),
        ('Cleaning', 'Clean-Up Drives'),
        ('Teaching', 'Community Teaching'),
        ('AnimalCare', 'Animal Welfare'),
        ('HealthCamp', 'Health Camps'),
        ('WasteMgmt', 'Waste Management'),
        ('WaterConservation', 'Water Conservation'),
        ('DisasterRelief', 'Disaster Relief'),
        ('ElderCare', 'Support for Elderly'),
        ('ChildWelfare', 'Child Welfare'),
        ('Fundraising', 'Fundraising'),
        ('Advocacy', 'Advocacy & Awareness'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    interests = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
    
class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=200,null=True, blank=True)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Donation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ₹{self.amount}"


class Volunteer(models.Model):

    INTEREST_CHOICES = [
        ('Planting', 'Tree Planting & Greening'),
        ('Cleaning', 'Clean-Up Drives'),
        ('Teaching', 'Community Teaching'),
        ('AnimalCare', 'Animal Welfare'),
        ('HealthCamp', 'Health Camps'),
        ('WasteMgmt', 'Waste Management'),
        ('WaterConservation', 'Water Conservation'),
        ('DisasterRelief', 'Disaster Relief'),
        ('ElderCare', 'Support for Elderly'),
        ('ChildWelfare', 'Child Welfare'),
        ('Fundraising', 'Fundraising'),
        ('Advocacy', 'Advocacy & Awareness'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.interest}"
    


class MobileApp(models.Model):
    apk_file = models.FileField(upload_to='apks/')
    version = models.CharField(max_length=20, default="1.0.0")
    release_notes = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Delete previous APK before saving new one
        if MobileApp.objects.exists():
            old_apk = MobileApp.objects.first()
            old_apk.apk_file.delete(save=False)
            old_apk.delete()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Version {self.version} uploaded at {self.uploaded_at}"
