from django.contrib.auth.models import (
  AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import Group, Permission 

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify



#:\Users\Swati\.virtualenvs\inst_mgmt-PblIhfcB\lib\ntpath.py
class UserManager(BaseUserManager):
    def create_user(
            self, email, mobile, name, city, password=None,
            commit=True, **kwargs):
        """
        Creates and saves a User with the given email, first name, last name
        and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not mobile:
            raise ValueError(_('Mobile number is necessary'))

        if not name :
            raise ValueError(_('Users must have a name'))

        user = self.model(
            email=self.normalize_email(email),
            mobile = mobile,
            name = name,
            city = city
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, name, password):
        """
        Creates and saves a superuser with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            mobile = mobile,
            name = name,
            password=password,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# import random

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    mobile = models.CharField(_("Mobile"), max_length=20, unique=True)
    name = models.CharField(_("Full Name"), max_length=180, blank=True, null=True)
    city = models.CharField(_("City"), max_length=100, blank=True, null=True)
    profile = models.ImageField(_("profile"), upload_to="profiles/", default="profiles/default/avtaar.jpg", blank=True, null=True)
    birth_date = models.DateField(_("Birth Date"), auto_now_add=False, null=True)
  
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', 'name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        # full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return self.name.strip()

    def __str__(self):
        return '{} <{}|{}>'.format(self.get_full_name(), self.email, self.mobile)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def save(self, *args, **kwargs): 
      super(User, self).save(*args, **kwargs)    
