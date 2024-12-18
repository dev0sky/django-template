from import_export import resources
from core.models import Log, Address, Email, Phone, Category, Date,CategoryImage,CategoryIcon

class PhoneResource(resources.ModelResource):
    class Meta:
        model = Phone
        fields = ('name', 'description', 'number', 'country', 'is_primary', 'content_type', 'object_id', 'content_object')

class AddressResource(resources.ModelResource):
    class Meta:
        model = Address
        fields = ('name', 'description', 'street', 'neighbourhood', 'number_int', 'number_ext','city','state', 'zip_code', 'country', 'object_id', 'content_object')
class EmailResource(resources.ModelResource):
    class Meta:
        model = Email
        fields = ('name', 'description', 'address')

class LogResource(resources.ModelResource):
    class Meta:
        model = Log
        fields = '__all__'

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = '__all__'

class DateResource(resources.ModelResource):
    class Meta:
        model = Date
        fields = ('id', 'date_name', 'date_description', 'start_at', 'end_at', 'status', 'created_at',
                  'updated_at')
        

class CategoryIconResource(resources.ModelResource):
    class Meta:
        model = CategoryIcon
        fields = '__all__'

class CategoryImageResource(resources.ModelResource):
    class Meta:
        model = CategoryImage
        fields = '__all__'
