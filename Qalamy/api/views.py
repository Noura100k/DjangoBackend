from rest_framework import viewsets
from ..models import Parents,Child,Challenges,Words,Letters,MyImage
from .serializers import ParentsModelSerializer, ChildModelSerializer,ChallengesModelSerializer,WordsModelSerializer,LettersModelSerializer,MyImageModelSerializer


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