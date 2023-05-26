from rest_framework import serializers
from ..models import Parents,Child,Challenges,Words,Letters,MyImage,MyVoiceParent,WordsExam,LettersExam,CorrectionWords,CorrectionLetters

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
        fields= ('id','chall_name','chall_type','grade','date','child_ID')

#Words---------------------------------///
class WordsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields= ('id','text','voice','image','letter_No','correction','chall_ID')

#Letters---------------------------------///
class LettersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letters
        fields= ('id','text','voice','image','correction','chall_ID')

#image---------------------------------///
class MyImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyImage
        fields= ('id','text')

#audio---------------------------------///
class MyVoiceParentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyVoiceParent
        fields= ('id','text','audio')


#new---------------------------------///
class WordsExamModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordsExam
        fields= ('id','text','voice','image','letter_No','challenges_ID')

#new---------------------------------///
class LettersExamModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LettersExam
        fields= ('id','text','voice','image','challenges_ID')
#new---------------------------------///
class CorrectionWordsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrectionWords
        fields= ('id','correction','words_ID')

#new---------------------------------///
class CorrectionLettersModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CorrectionLetters
        fields= ('id','correction','letter_ID')
