from django.contrib import admin
from .models import Parents,Child,Challenges,Words,Letters,MyImage,MyVoiceParent,WordsExam,LettersExam,CorrectionWords,CorrectionLetters
# Register your models here.

admin.site.register(Parents)
admin.site.register(Child)
admin.site.register(Challenges)
admin.site.register(Words)
admin.site.register(Letters)
admin.site.register(MyImage)
admin.site.register(MyVoiceParent)
admin.site.register(WordsExam)
admin.site.register(LettersExam)
admin.site.register(CorrectionWords)
admin.site.register(CorrectionLetters)