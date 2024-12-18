from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address.'))
        if not password:
            raise ValueError(_('Users must have a password.'))
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff, 
            is_active=True,
            is_superuser=is_superuser, 
            last_login=None,
            date_joined=now, 
            role='contributor',
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user=self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    USER_ROLE_CHOICES = [
        ('client', 'Client'),
        ('contributor', 'Contributor'),
    ]
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='client')
    
    objects = UserManager()
    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)
    
class UserSettings(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='usersettings_fk_user')
    preferred_language = models.CharField(
        max_length=10,
        choices=[
            ('de', _('Deutsch')),
            ('en', _('English')),
            ('es', _('Español')),
            ('fr', _('Français')),
            ('it', _('Italiano')),
            ('ja', _('日本語')),
            ('ko', _('韓国語')),
            ('pt', _('Português')),
            ('zh', _('中国人')),
        ],
        default='es',
        verbose_name=_('Preferred Language')
    )
    analytical_cookies = models.BooleanField(
        default=True,
        verbose_name=_('Analytical Cookies'),
        help_text=_('Allow analytical cookies for site statistics.')
    )
    functionality_cookies = models.BooleanField(
        default=True,
        verbose_name=_('Functionality Cookies'),
        help_text=_('Allow functionality cookies for improved site functionality.')
    )
    advertising_cookies = models.BooleanField(
        default=False,
        verbose_name=_('Advertising Cookies'),
        help_text=_('Allow advertising cookies for personalized ads.')
    )
    theme_preference = models.CharField(
        max_length=10,
        choices=[
            ('light', _('Light')),
            ('dark', _('Dark')),
            ('oled', _('OLED')),
        ],
        default='light',
        verbose_name=_('Theme Preference')
    )
    
    class Meta:
        verbose_name = _('User Settings')
        verbose_name_plural = _('User Settings')

    def __str__(self):
        return self.user.username + "'s Settings"
