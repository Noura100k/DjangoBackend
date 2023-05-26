from rest_framework import routers
from .views import ParentsViewSet,ChildViewSet,ChallengesViewSet,WordsViewSet,LettersViewSet,MyImageViewSet,MyVoiceParentViewSet,WordsExamViewSet,LettersExamViewSet,CorrectionWordsViewSet,CorrectionLettersViewSet
from django.urls import path,include

router = routers.DefaultRouter()
router.register(r'Parents',ParentsViewSet)
router.register(r'Child',ChildViewSet)
router.register(r'Challenges',ChallengesViewSet)
router.register(r'Words',WordsViewSet)
router.register(r'Letters',LettersViewSet)
router.register(r'MyImage',MyImageViewSet)
router.register(r'MyVoiceParent',MyVoiceParentViewSet)
router.register(r'WordsExam',WordsExamViewSet)
router.register(r'LettersExam',LettersExamViewSet)
router.register(r'CorrectionWords',CorrectionWordsViewSet)
router.register(r'CorrectionLetters',CorrectionLettersViewSet)
urlpatterns=[

path('',include(router.urls))
    
]