
from persons.models import Person
from rest_framework import serializers
 
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'  

class PersonNoSensibleInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'birth', 'is_active', 'country'] 