from rest_framework import routers
from .views import ParentsViewSet,ChildViewSet,ChallengesViewSet,WordsViewSet,LettersViewSet,MyImageViewSet,MyVoiceParentViewSet
from django.urls import path,include

router = routers.DefaultRouter()
router.register(r'Parents',ParentsViewSet)
router.register(r'Child',ChildViewSet)
router.register(r'Challenges',ChallengesViewSet)
router.register(r'Words',WordsViewSet)
router.register(r'Letters',LettersViewSet)
router.register(r'MyImage',MyImageViewSet)
router.register(r'MyVoiceParent',MyVoiceParentViewSet)
urlpatterns=[

path('',include(router.urls))
    
]