from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from social_network.models import Timestamped
from user.utils import generate_secure_password
from datetime import date

class UserProfile(Timestamped):
    GENDER_CHOICES = [('Male', 'Male'),('Female', 'Female'),('Other', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    interests = models.TextField(blank=True)
    about = models.TextField(blank=True)

    def clean(self, *args, **kwargs):
        if not self.email:
            raise ValidationError("Email field is mandatory for registration")
        if self.email:
            email_validator = EmailValidator()
            email_validator(self.email)
        if self.date_of_birth:
            min_age = 18
            age = (date.today() - self.date_of_birth).days // 365
            if age < min_age:
                raise ValidationError(f"You must be at least {min_age} years old.")
                
    def save(self, *args, **kwargs):
        if not self.id:
            self.user = User.objects.create_user(
                username=self.email,
                email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=generate_secure_password()
            )
        else:
            self.user.email = self.email
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()
            if self.password:
                self.user.set_password(self.password)
        super(UserProfile, self).save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self):
        return self.email
    

class BlockedProfile(Timestamped):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='blocked_user')
    blocked_profile = models.ManyToManyField(UserProfile, related_name='blocked_by')

    @property
    def blocked_profile_ids(self):
        return self.blocked_profile.values_list("id", flat=True)

    def __str__(self):
        return self.user.username