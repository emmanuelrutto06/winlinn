from django.db import models
from django.utils.timezone import datetime, timedelta
import django.utils.timezone
from django.conf import settings
from django_countries.fields import CountryField

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)

from django.db.models.signals import post_save
from django.dispatch import receiver



# stripe.api_key=settings.STRIPE_SECRET_KEY
# Create your models here.


# class UserManager(BaseUserManager):
#     """
#     Django requires that custom users define their own Manager class. By
#     inheriting from `BaseUserManager`, we get a lot of the same code used by
#     Django to create a `User` for free.
#     All we have to do is override the `create_user` function which we will use
#     to create `User` objects.
#     """

#     def create_user(self, *args, **kwargs):
#         """Create and return a `User` with an email, username and password."""
#         password = kwargs.get('password', '')
#         email = kwargs.get('email', '')
#         del kwargs['email']
#         del kwargs['password']
#         user = self.model(email=self.normalize_email(email), **kwargs)
#         user.set_password(password)
#         user.save()

#         return user

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    first_name = models.CharField(db_index=True, max_length=255, unique=False)
    last_name = models.CharField(db_index=True, max_length=255, unique=False)
    username = models.CharField(db_index=True, max_length=255, unique=False,null=True,blank=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_client=models.BooleanField(' Check the checkbox alongside to signup as Client',default=False)
    is_administrator=models.BooleanField(' Check the checkbox alongside to signup as an Administrator',default=False)
    is_superuser=models.BooleanField(default=False)
    is_staff = models.BooleanField('staff status',default=False)
    date_of_birth = models.DateTimeField(null=True,blank=True,default=django.utils.timezone.now)
    phone=models.CharField(max_length=200,null=True,blank=True)
    additional_phone=models.CharField(max_length=200,null=True,blank=True)
    country = models.CharField(db_index=True, max_length=255, unique=False)
    time_zone=models.CharField(max_length=200,null=True,blank=True)
    night_calls=models.BooleanField(default=False,null=True,blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=200, null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','is_administrator']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return str(self.username) 

    @property
    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name. Since we do not store
        the user's real name, we return their username instead.
        """
        return self.first_name


class Client(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)


class Adminstration(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)


class Notification(models.Model):
    title=models.CharField(max_length=256)
    message=models.TextField()
    viewed=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
 

@receiver(post_save,sender=User)
def create_welcome_message(sender,instance,**kwargs):
    if kwargs['created']:
        Notification.objects.create(
            user=instance,
            title='Welcome to WinLinMac Tutorials',
            message='A new user has clocked in',
        )
        