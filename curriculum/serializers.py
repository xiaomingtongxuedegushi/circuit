from rest_framework import serializers
from curriculum.models import Course, Resources


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Course
        fields = '__all__'


class ResourcesSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 0
        model = Resources
        fields = '__all__'
