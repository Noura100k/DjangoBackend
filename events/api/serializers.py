from rest_framework import serializers
from ..models import Event
#http://127.0.0.1:8000/api/events/
class EventModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields= ('id','name','description','qr_code','date')
