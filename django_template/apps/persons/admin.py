from django.contrib import admin
from persons.resources import PersonResource 
from import_export.admin import ImportExportModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from persons.models import  Person
from core.models import  Phone, Address

class PhoneInline(GenericTabularInline):
    model = Phone
    extra = 0

class AddressInline(GenericTabularInline):
    model = Address
    extra = 0

@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    resource_class = PersonResource
    list_display = ('name', 'middle_name', 'fathers_last_name', 'mothers_last_name', 'birth', 'created_at', 'updated_at', 'is_active')
    list_filter = ('country', 'is_active')
    search_fields = ('name', 'middle_name', 'fathers_last_name', 'mothers_last_name', 'rfc')
    inlines = [PhoneInline, AddressInline]
