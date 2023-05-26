from rest_framework import viewsets
from ..models import Parents,Child,Challenges,Words,Letters,MyImage,MyVoiceParent,WordsExam,LettersExam,CorrectionWords,CorrectionLetters
from .serializers import ParentsModelSerializer, ChildModelSerializer,ChallengesModelSerializer,WordsModelSerializer,LettersModelSerializer,MyImageModelSerializer, MyVoiceParentModelSerializer,WordsExamModelSerializer,LettersExamModelSerializer,CorrectionWordsModelSerializer,CorrectionLettersModelSerializer


#parent----------------------------//
class ParentsViewSet(viewsets.ModelViewSet):
    queryset=Parents.objects.all()
    serializer_class=ParentsModelSerializer



#child-------------------------------//
class ChildViewSet(viewsets.ModelViewSet):
    queryset=Child.objects.all()
    serializer_class=ChildModelSerializer


#challenges--------------------------//
class ChallengesViewSet(viewsets.ModelViewSet):
    queryset=Challenges.objects.all()
    serializer_class=ChallengesModelSerializer


#words-------------------------------//
class WordsViewSet(viewsets.ModelViewSet):
    queryset=Words.objects.all()
    serializer_class=WordsModelSerializer


#letters-----------------------------//

class LettersViewSet(viewsets.ModelViewSet):
    queryset=Letters.objects.all()
    serializer_class=LettersModelSerializer



#image-----------------------------//

class MyImageViewSet(viewsets.ModelViewSet):
    queryset=MyImage.objects.all()
    serializer_class=MyImageModelSerializer

#voice-----------------------------//

class MyVoiceParentViewSet(viewsets.ModelViewSet):
    queryset=MyVoiceParent.objects.all()
    serializer_class=MyVoiceParentModelSerializer


#new-----------------------------//

class WordsExamViewSet(viewsets.ModelViewSet):
    queryset=WordsExam.objects.all()
    serializer_class=WordsExamModelSerializer


#new-----------------------------//

class LettersExamViewSet(viewsets.ModelViewSet):
    queryset=LettersExam.objects.all()
    serializer_class=LettersExamModelSerializer



#new-----------------------------//

class CorrectionWordsViewSet(viewsets.ModelViewSet):
    queryset=CorrectionWords.objects.all()
    serializer_class=CorrectionWordsModelSerializer


#new-----------------------------//

class CorrectionLettersViewSet(viewsets.ModelViewSet):
    queryset=CorrectionLetters.objects.all()
    serializer_class=CorrectionLettersModelSerializer