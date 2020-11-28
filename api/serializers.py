from rest_framework import serializers
from .models import EarthQuake


class EarthQuakeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = EarthQuake
