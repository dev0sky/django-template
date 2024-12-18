
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from core.models import Thing, Phone, Address, Log, PhysicalObject, Category


# CATEGORIES
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = '__all__'


