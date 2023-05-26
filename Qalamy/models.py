from django.db import models
import qrcode
from io import BytesIO

# Create your models here.

# Parents--------------------//
class Parents(models.Model):
    name=models.CharField(blank=True,max_length=200)
    email=models.EmailField(max_length = 254,unique=True)
    password=models.CharField(max_length=50,blank=True)

    #has=models.ManyToManyField(Child)

    def __str__(self):
        return str(self.name)

# Child--------------------//
class Child(models.Model):
    name=models.CharField(max_length=200,blank=True)
    username=models.CharField(max_length=200,unique=True)
    sex=models.CharField(max_length = 200,blank=True)
    age=models.IntegerField()
    image=models.ImageField(blank=True, upload_to='qrcodes/')
    password=models.CharField(max_length=50,blank=True)
    parent_ID=models.ForeignKey(Parents, on_delete=models.CASCADE)
    #has=models.ManyToManyField(Challenges)

    def __str__(self):
        return str(self.name)


# Challenges----------------//

class Challenges(models.Model):
    chall_name=models.CharField(max_length=200,blank=True)
    chall_type=models.CharField(max_length=200,blank=True)
    grade=models.IntegerField()
    date=models.TextField(max_length=200,blank=True)
    child_ID=models.ForeignKey(Child, on_delete=models.CASCADE)
    #contain_letters=models.ManyToManyField(Letters)
    #contain_words=models.ManyToManyField(words)
    def __str__(self):
        return str(self.chall_name)


# words-------------------//
# l need to fix voice type
class Words(models.Model):
    text=models.TextField(max_length=200,blank=True)
    voice=models.FileField( upload_to ='qrcodes/',blank=True)
    image=models.ImageField(blank=True, upload_to='qrcodes/')
    letter_No=models.IntegerField()
    chall_ID=models.ForeignKey(Challenges, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)

# Letters-----------------//
class Letters(models.Model):
    text=models.TextField(max_length=200,blank=True)
    voice=models.FileField( upload_to ='qrcodes/',blank=True)
    image=models.ImageField(blank=True, upload_to='qrcodes/')
    chall_ID=models.ForeignKey(Challenges, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)

# image-----------------//
class MyImage(models.Model):
    text=models.TextField(max_length=200)

    def __str__(self):
        return str(self.text)


# image-----------------//
class MyVoiceParent(models.Model):
    audio=models.FileField( upload_to ='qrcodes/',blank=True)
    text=models.TextField(max_length=200)

    def __str__(self):
        return str(self.text)

# new for test

class WordsExam(models.Model):
    text=models.TextField(max_length=200,blank=True)
    voice=models.FileField( upload_to ='qrcodes/',blank=True)
    image=models.ImageField(blank=True, upload_to='qrcodes/')
    letter_No=models.IntegerField()
    challenges_ID=models.ForeignKey(Challenges, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)

# Letters-----------------//
class LettersExam(models.Model):
    text=models.TextField(max_length=200,blank=True)
    voice=models.FileField( upload_to ='qrcodes/',blank=True)
    image=models.ImageField(blank=True, upload_to='qrcodes/')
    challenges_ID=models.ForeignKey(Challenges, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)


class CorrectionLetters(models.Model):
    correction=models.IntegerField()
    letter_ID=models.ForeignKey(LettersExam, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.correction)

class CorrectionWords(models.Model):
    correction=models.IntegerField()
    words_ID=models.ForeignKey(WordsExam, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.correction)