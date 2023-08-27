from django.db import models
from django.db.models import Q
from django.contrib.auth.models import UserManager, AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from social_network.models import Timestamped
from user.utils import generate_secure_password
from django.contrib.auth.models import User
from datetime import date
from django.utils.translation import gettext as _

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class UserProfileManager(models.Manager):
    def create_userprofile_with_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is mandatory for registration")
        is_auto_generated_password = False
        if not password:
            is_auto_generated_password = True
            password = generate_secure_password()
        user = User.objects.create_user(email=email, password=password)
        user_profile = self.model(user=user, **kwargs)
        user_profile.is_auto_generated_password = is_auto_generated_password
        user_profile.save()
        return user_profile

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',  # Change this to a unique name
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_set',  # Change this to a unique name
        related_query_name='custom_user'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    objects = CustomUserManager()

    # class Meta:
    #     swappable = 'AUTH_USER_MODEL'

# CustomUser._meta.get_field('groups').related_query_name = 'custom_user_groups'
# CustomUser._meta.get_field('user_permissions').related_query_name = 'custom_user_permissions'


# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True, db_index=True)


#     USERNAME_FIELD = 'email'
#     objects = UserManager()

#     def __str__(self):
#         return self.email

class UserProfile(Timestamped):
    GENDER_CHOICES = [('Male', 'Male'),('Female', 'Female'),('Other', 'Other')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True, db_index=True)
    interests = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)

    objects = UserProfileManager()

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
    
    @property
    def friend_list(self):
        return self.friendships_as_user1.all() | self.friendships_as_user2.all()

    def has_friendship_with(self, user_profile):
        return self.friend_list.filter(Q(user1 = user_profile) | Q(user2=user_profile)).exists()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()
    
class BlockedProfile(Timestamped):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='blocked_user')
    blocked_profile = models.ManyToManyField(UserProfile, related_name='blocked_by')

    @property
    def blocked_profile_ids(self):
        return self.blocked_profile.values_list("id", flat=True)

    def __str__(self):
        return self.user.username