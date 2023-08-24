from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from user.utils import generate_secure_password
from datetime import date

class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Male'),('F', 'Female'),('O', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    interests = models.TextField(blank=True)
    about = models.TextField(blank=True)

    def clean(self, *args, **kwargs):
        if self.date_of_birth:
            min_age = 18
            age = (date.today() - self.date_of_birth).days // 365
            if age < min_age:
                raise ValidationError(f"You must be at least {min_age} years old.")

        if not self.email:
            raise ValidationError("Email field is mandatory for registration")
        if self.email:
            email_validator = EmailValidator()
            email_validator(self.email)
                
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
    
