from rest_framework import serializers
from .models import Application
from rest_framework import serializers

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class ApplicationPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('name', 'submitted_at', 'phone_num', 'date_of_birth')