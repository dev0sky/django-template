from django.contrib import admin
from core.admin_utils import log_admin_action
from import_export.admin import ImportExportModelAdmin
from core.models import Phone, Address,Email, Log, Category, Date, CategoryIcon, CategoryImage
from core.resources import LogResource, AddressResource, PhoneResource, DateResource,CategoryIconResource,CategoryImageResource, EmailResource

class CategoryImageInline(admin.StackedInline):
    model = CategoryImage
    extra = 0

class CategoryIconInline(admin.StackedInline):
    model = CategoryIcon
    extra = 0

class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 0

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0
    
class EmailInline(admin.StackedInline):
    model = Email
    extra = 0

@admin.register(Phone)
class PhoneAdmin(ImportExportModelAdmin):
    resource_class = PhoneResource
    list_display = ('name', 'description', 'number', 'is_primary', 'content_object')
    list_filter = ( 'is_primary',)
    search_fields = ('name','description', 'number', 'content_object__name')
    def save_model(self, request, obj, form, change):
        log_admin_action(request, obj, form, change)
        super().save_model(request, obj, form, change)

@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin):
    resource_class = AddressResource
    list_display = ('name','description', 'street', 'neighbourhood','number_int','number_ext','city', 'state', 'zip_code', 'country', 'content_object')
    list_filter = ('country',)
    search_fields = ('name','description', 'street', 'city', 'neighbourhood','number_int','number_ext','state', 'zip_code', 'content_object__name')
    def save_model(self, request, obj, form, change):
        log_admin_action(request, obj, form, change)
        super().save_model(request, obj, form, change)

@admin.register(Email)
class EmailAdmin(ImportExportModelAdmin):
    resource_class = EmailResource
    list_display = ('name','description', 'address')
    list_filter = ('address',)
    search_fields = ('name','description', 'address', )
    def save_model(self, request, obj, form, change):
        log_admin_action(request, obj, form, change)
        super().save_model(request, obj, form, change)

@admin.register(Log)
class LogAdmin(ImportExportModelAdmin):
    resource_class = LogResource
    list_display = ('name', 'description','model', 'log_type','user','ip_address','created_at',)
    list_filter = ('created_at', 'log_type','model', 'user')
    search_fields = ('name','description', 'model','log_type','user','ip_address','created_at',)
    autocomplete_fields = ['user',]

@admin.register(Date)
class DateAdmin(ImportExportModelAdmin):
    resource_class = DateResource
    list_display = ('name','description','start_at', 'end_at')
    # list_filter = ()
    search_fields = ('name','description')

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = Category
    list_display = ('name','description', 'key')
    # list_filter = ()
    search_fields = ('name','description', 'key')
    autocomplete_fields = ['thematic_areas',]
    inlines = [ CategoryImageInline, CategoryIconInline]
    def save_model(self, request, obj, form, change):
        log_admin_action(request, obj, form, change)
        super().save_model(request, obj, form, change)

@admin.register(CategoryIcon)
class CategoryIconAdmin(ImportExportModelAdmin):
    resource_class = CategoryIconResource
    list_display = ('name','description', 'type')
    list_filter = ('type',)
    search_fields = ('name','description','type')
    def save_model(self, request, obj, form, change):
        log_admin_action(request, obj, form, change)
        super().save_model(request, obj, form, change)

@admin.register(CategoryImage)
class CategoryImageAdmin(ImportExportModelAdmin):
    resource_class = CategoryImageResource
    list_display = ('name','description', 'type')
    list_filter = ('type',)
    search_fields = ('name','description','type')
    def save_model(self, request, obj, form, change):
        log_admin_action(request, obj, form, change)
        super().save_model(request, obj, form, change)
