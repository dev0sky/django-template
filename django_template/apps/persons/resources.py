from import_export import resources
from persons.models import Person

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person

