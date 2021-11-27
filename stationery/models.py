# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class Room(models.Model):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=10)

class Registrations(models.Model):
    room = models.ForeignKey('Room', on_delete=models.PROTECT, null=True)

    QUARTER = [(1, 'Quy 1'),(2, 'Quy 2'),(3, 'Quy 3'), (4, 'Quy 4')]
    quarter = models.SmallIntegerField(choices=QUARTER, null=True)

    STATUS = [(1, 'New'),(2, 'Approved'),(3, 'Rejected')]
    status = models.SmallIntegerField(choices=STATUS, null=True)


class Stationery(models.Model):
    name = models.CharField(max_length=60)
    unit = models.ForeignKey('Unit', on_delete=models.PROTECT, null=True)

class Unit(models.Model):
    name = models.CharField(max_length=60)

class Regist_detail(models.Model):
    registration = models.ForeignKey('Registrations', on_delete=models.PROTECT, null=True)
    stationery = models.ForeignKey('Stationery', on_delete=models.PROTECT, null=True)
    amount=models.IntegerField()
    total = models.IntegerField()

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    room = models.ForeignKey('Room', on_delete=models.PROTECT, null=True)
    
    ROLES = [(0, 'Admin'),(1, 'Manager'),(2, 'Staff')]
    role = models.SmallIntegerField(choices=ROLES, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    