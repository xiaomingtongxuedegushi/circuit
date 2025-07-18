from rest_framework import serializers
from electron.models import elecontest



class elecontestSerializer(serializers.ModelSerializer):
    class Meta:
        start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
        depth = 0
        model = elecontest
        fields = '__all__'
