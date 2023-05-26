from rest_framework import serializers
from .models import Group, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        
        model = Group
        fields = '__all__'






