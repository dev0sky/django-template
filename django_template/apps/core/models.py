# -*- coding: utf-8 -*-
from django.db import models
from colorfield.fields import ColorField
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Thing(models.Model):
    name = models.CharField(null=False, default='', max_length=256, verbose_name=_('Name'))                                                                
    description = models.TextField(null=True, verbose_name=_('Description'))  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Updated At'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        
class Phone(Thing):
    country = CountryField(null=False, verbose_name=_('Country'))
    number = models.CharField(null=False, max_length=10, verbose_name=_('Number'))
    is_primary = models.BooleanField(null=False, default=True, verbose_name=_('Main'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='phone_fk_content_type', verbose_name=_('Content Type'))
    object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    number_regex = r'^\+?\d{1,4} ?\d{1,3} ?\d{1,3} ?\d{1,4}$'
    number_validator = RegexValidator(
        regex=number_regex,
        message=_('The phone number must have a valid format.'),
        code='invalid_phone'
    )
    number = models.CharField(
        max_length=10,
        validators=[number_validator],
        help_text=_('Enter the phone number in international format (optional) and without dashes.'),
    ) 

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = _('Phone')
        verbose_name_plural = _('Phones')

class Address(Thing):
    street = models.CharField(null=False, max_length=100, verbose_name=_('Street'))
    neighbourhood = models.CharField(null=False, max_length=100, verbose_name=_('Neighbourhood'))
    number_int = models.IntegerField(null=False, verbose_name=_('Exterior number'))
    number_ext = models.IntegerField(null=True, verbose_name=_('Internal number'))
    city = models.CharField(null=False, max_length=100, verbose_name=_('City'))
    state = models.CharField(null=False, max_length=100, verbose_name=_('State'))
    zip_code = models.CharField(null=False, max_length=20, verbose_name=_('ZIP code'))
    country = CountryField(null=False, verbose_name=_('Country'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='address_fk_content_type', verbose_name=_('Content Type'))
    object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}'

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

class Email(Thing):
    address = models.CharField(null=False, max_length=100, verbose_name=_('Address'))

    def __str__(self):
        return f'{self.street}, {self.city}, {self.state}, {self.zip_code}, {self.country}'

    class Meta:
        
        verbose_name = _('Email')
        verbose_name_plural = _('Emails')

class Log(Thing):
    LOG_TYPES = [
        ('create', _('Create')),
        ('update', _('Update')),
        ('deactivate', _('Deactivate')),
        ('delete', _('Delete')),
        ('other', _('Other')),
    ]

    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, verbose_name=_('User'))
    model = models.CharField(max_length=48, verbose_name=_('Model'))
    log_type = models.CharField(null=False, max_length=10, choices=LOG_TYPES, verbose_name=_('Log Type'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP Address'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='log_fk_content_type', verbose_name=_('Content Type'))
    object_id = models.PositiveIntegerField(verbose_name=_('Object ID'))
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f'{self.log_type} - {self.name}' 

class PhysicalObject(models.Model):
    height = models.DecimalField(null=True, max_digits=8, decimal_places=2, default='0.0', verbose_name=_('Height'))  
    height_uom = models.ForeignKey('core.UnitOfMeasurement', on_delete=models.CASCADE, related_name='physicalobject_fk_height_uom', verbose_name=_('Height UOM'), help_text=_('Unit of measurement for height'), null=True, blank=True)                                                              
    width = models.DecimalField(null=True, max_digits=8, decimal_places=2, default='0.0', verbose_name=_('Width'))   
    width_uom = models.ForeignKey('core.UnitOfMeasurement', on_delete=models.CASCADE, related_name='physicalobject_fk_width_uom', verbose_name=_('Width UOM'), help_text=_('Unit of measurement for width'), null=True, blank=True)                                                             
    lenght = models.DecimalField(null=True, max_digits=8, decimal_places=2, default='0.0', verbose_name=_('Lenght'))                                                                
    lenght_uom = models.ForeignKey('core.UnitOfMeasurement', on_delete=models.CASCADE, related_name='physicalobject_fk_lenght_uom', verbose_name=_('Lenght UOM'), help_text=_('Unit of measurement for lenght'), null=True, blank=True)
    volume = models.DecimalField(null=True, max_digits=8, decimal_places=2, default='0.0', verbose_name=_('Volume'))  
    volume_uom = models.ForeignKey('core.UnitOfMeasurement', on_delete=models.CASCADE, related_name='physicalobject_fk_volume_uom', verbose_name=_('Volume UOM'), help_text=_('Unit of measurement for volume'), null=True, blank=True)
    
    class Meta:
        abstract = True

class Topic(Thing):
    code = models.CharField(null=False, max_length=24, verbose_name=_('Code'))

    def __str__(self):
        return f'{self.code} - {self.name}'
    
    class Meta:
        verbose_name = _('Thematic Area')
        verbose_name_plural = _('Thematic Areas')
        ordering = ['code',]
    
class Category(Thing):
    topic = models.ManyToManyField('core.Topic', related_name='category_fk_thematic_areas',  verbose_name=_('Topic'))
    key = models.CharField(null=False, max_length=48,verbose_name=_('Category Key'))
    is_popular = models.BooleanField(default=False, verbose_name=_('Is Popular'))
    color = ColorField(default='#FFFFFF', verbose_name=_('Emphasis'))
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='parentcategory_fk_category', verbose_name=_('Parent Category'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name', 'is_popular',]

class Date(Thing):
    STATUS_CHOICES = [
        ('created', _('Created')),
        ('in_progress', _('In progress')),
        ('ended', _('Ended')),
        ('cancelled', _('Cancelled')),
    ]
    
    start_at = models.DateTimeField(null=False, verbose_name=_('Start At'))
    end_at = models.DateTimeField(null=True, verbose_name=_('End At'))
    status = models.CharField(null=False, max_length=20, choices=STATUS_CHOICES, default='created', verbose_name=_('Status'))

    def __str__(self):
        return str(self.name)

class Image(Thing):
    IMAGE_TYPES = [
        ('cover', 'Cover'),
        ('wallpaper', 'Wallpaper'),
        ('advertising', 'Advertising'),
        ('default', 'default'),
        ('other', 'Other'),
    ]

    alt_text = models.CharField(null=False, max_length=255, verbose_name=_('Alt Text'))
    image = models.ImageField(null=False, upload_to='images/', verbose_name=_('Image'))
    type = models.CharField(null=False, max_length=20, default='default', choices=IMAGE_TYPES, verbose_name=_('Image Type'))

    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

class CategoryIcon(Image):
    category = models.ForeignKey('core.Category', on_delete=models.CASCADE, related_name='categoryicon_fk_category', verbose_name=_('Category'))

    def get_storage_path(self, filename):
        return f'images/apps/categories/{self.category.name}/{self.type}/{filename}'
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category Icon')
        verbose_name_plural = _('Category Icons')

class CategoryImage(Image):
    category = models.ForeignKey('core.Category', on_delete=models.CASCADE, related_name='categoryimage_fk_category', verbose_name=_('Category'))

    def get_storage_path(self, filename):
        return f'images/apps/categories/{self.category.name}/{self.type}/{filename}'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Category Image')
        verbose_name_plural = _('Category Images')

class UnitOfMeasurement(Thing):
    key = models.CharField(null=False, max_length=128, verbose_name=_('Key'))
    type_of = models.CharField(null=False, max_length=128, verbose_name=_('Type'))

    def __str__(self):
        return f'{self.name} - {self.type_of}'
    
    class Meta:
        verbose_name = _('Unit of Measurement')
        verbose_name_plural = _('Units of Measurement')
        ordering = ['type_of',]