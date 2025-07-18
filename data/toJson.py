from rest_framework import serializers
from data.models import Fault

class Fault_data(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Fault
        fields ='__all__'