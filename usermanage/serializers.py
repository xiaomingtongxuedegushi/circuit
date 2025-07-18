from rest_framework import serializers
from usermanage.models import Students,Classes


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Students
        fields = '__all__'

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 0
        model = Classes
        fields = '__all__'