from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class CustomManager(BaseUserManager):
    def create_user(self, email, user_name, password, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verify', True)
        extra_fields.setdefault('user_type', 'developer')

        if extra_fields.setdefault('is_staff') is not True:
            raise ValueError('superuser must be is_staff=true')
        if extra_fields.setdefault('is_superuser') is not True:
            raise ValueError('superuser must be is_superuser=true')
        if extra_fields.setdefault('is_active') is not True:
            raise ValueError('superuser must be is_active=true')
        if extra_fields.setdefault('is_verify') is not True:
            raise ValueError('superuser must be is_verify=true')

        return self.create_user(email, user_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('visitor', 'visitor'),
        ('developer', 'developer'),
    )
    email = models.EmailField(max_length=254, unique=True)
    user_name = models.CharField(max_length=100, unique=True)

    REQUIRED_FIELDS = ['user_name',]
    USERNAME_FIELD = 'email'
    user_type = models.CharField(
        max_length=50,  choices=USER_TYPE, default=USER_TYPE[0])
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)

    objects = CustomManager()

    def __str__(self):
        return str(self.email)


class Profile(models.Model):
    user = models.OneToOneField(
        "App_account.User", related_name='user_profile', on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=False, null=False)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    date_join = models.DateTimeField( auto_now_add=True)
    
    def __str__(self):
        return str(self.user.user_name)
    

    def save(self, *args, **kwargs):
        user_email = self.user.email
        split_username = user_email.index('@')
        get_username = user_email[:split_username]
        self.username = get_username
        return super().save(*args, **kwargs)
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.user_profile.save()