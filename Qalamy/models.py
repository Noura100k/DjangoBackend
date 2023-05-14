from django.db import models
import qrcode
from io import BytesIO

# Create your models here.

# Parents--------------------//
class Parents(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length = 254)
    password=models.CharField(max_length=50)

    #has=models.ManyToManyField(Child)

    def __str__(self):
        return str(self.name)

# Child--------------------//
class Child(models.Model):
    name=models.CharField(max_length=200)
    username=models.CharField(max_length=200)
    sex=models.CharField(max_length = 200)
    age=models.IntegerField()
    image=models.ImageField(blank=True, upload_to='qrcodes/')
    password=models.CharField(max_length=50)
    parent_ID=models.ForeignKey(Parents, on_delete=models.CASCADE)
    #has=models.ManyToManyField(Challenges)

    def __str__(self):
        return str(self.name)


# Challenges----------------//

class Challenges(models.Model):
    chall_name=models.CharField(max_length=200)
    chall_type=models.CharField(max_length=200)
    grade=models.IntegerField()
    date=models.DateField()
    parent_ID=models.ForeignKey(Parents, on_delete=models.CASCADE)
    child_ID=models.ForeignKey(Child, on_delete=models.CASCADE)
    #contain_letters=models.ManyToManyField(Letters)
    #contain_words=models.ManyToManyField(words)
    def __str__(self):
        return str(self.chall_name)


# words-------------------//
# l need to fix voice type
class Words(models.Model):
    text=models.TextField(max_length=200)
    voice=models.TextField(max_length=200)
    image=models.ImageField(blank=True, upload_to='qrcodes/')
    letter_No=models.IntegerField()
    correction=models.IntegerField()
    child_ID=models.ForeignKey(Child, on_delete=models.CASCADE)
    chall_ID=models.ForeignKey(Challenges, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)

# Letters-----------------//
class Letters(models.Model):
    text=models.TextField(max_length=200)
    voice=models.TextField(max_length=200)
    image=models.ImageField(blank=True, upload_to='qrcodes/')
    correction=models.IntegerField()
    child_ID=models.ForeignKey(Child, on_delete=models.CASCADE)
    chall_ID=models.ForeignKey(Challenges, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.text)

# image-----------------//
class MyImage(models.Model):
    text=models.TextField(max_length=200)
    image = models.ImageField(blank=True, upload_to='qrcodes/')
    def __str__(self):
        return str(self.text)

