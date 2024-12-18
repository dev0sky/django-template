# -*- coding: utf-8 -*-
from django.db import models
from core.models import Phone, Address
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation



class Person(models.Model):
    country = CountryField(null=False, verbose_name=_('Country'))
    name = models.CharField(max_length=100,null=False, verbose_name=_('Name'))
    middle_name = models.CharField(max_length=50,blank=True, verbose_name=_('Middle Name'), default='')
    fathers_last_name = models.CharField(max_length=50,null=True, verbose_name=_("Father's Lastname"))
    mothers_last_name = models.CharField(max_length=50,blank=True, verbose_name=_("Mother's Lastname"))
    birth = models.DateField(default='1900-01-01', verbose_name=_('Birth date'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    
    phones = GenericRelation(Phone)
    addresses = GenericRelation(Address)
    rfc_regex = r'^[A-ZÑ&]{3,4}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[A-Z0-9Ñ&]{3}$'
    rfc = models.CharField(max_length=13, validators=[RegexValidator(regex=rfc_regex)], blank=True, null=True)
    
    def __str__(self):
        full_name = self.name
        if self.middle_name:
            full_name += ' ' + self.middle_name
        if self.fathers_last_name:
            full_name += ' ' + self.fathers_last_name
        if self.mothers_last_name:
            full_name += ' ' + self.mothers_last_name
        return full_name

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        ordering = ['country', 'fathers_last_name', 'mothers_last_name', 'name', 'middle_name', 'birth']


