from rest_framework import serializers
from ..models import Parents,Child,Challenges,Words,Letters,MyImage

#http://127.0.0.1:8000/api/Parents/

#parents------------------------------///
class ParentsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields= ('id','name','email','password')
      

#child---------------------------------///
class ChildModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Child
        fields= ('id','name','username','sex','age','image','password','parent_ID')

#Challenges---------------------------------///
class ChallengesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenges
        fields= ('id','chall_name','chall_type','grade','date','parent_ID','child_ID')

#Words---------------------------------///
class WordsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields= ('id','text','voice','image','letter_No','correction','child_ID','chall_ID')

#Letters---------------------------------///
class LettersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letters
        fields= ('id','text','voice','image','correction','child_ID','chall_ID')

#image---------------------------------///
class MyImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyImage
        fields= ('id','text')

