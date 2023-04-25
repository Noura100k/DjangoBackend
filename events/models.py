from django.db import models
import qrcode
from io import BytesIO

# Create your models here.
class Event(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    qr_code=models.ImageField(blank=True, upload_to='qrcodes/')
    date=models.DateField()

    def __str__(self):
        return str(self.name)
    
 



