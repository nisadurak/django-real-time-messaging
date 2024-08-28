from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User

class Calisan(models.Model):
    calisanid = models.CharField(max_length=20, primary_key=True,default='default_value')
    isim = models.CharField(max_length=100)
    soyisim = models.CharField(max_length=100)
    telefonturu = models.CharField(max_length=100, default='Girilmedi')
    telefon = models.CharField(max_length=15, default='000 000 00 00')
    mail = models.EmailField(default='example@example.com', unique=False,verbose_name=("mail"))
    departman = models.CharField(max_length=100, default='Girilmedi')
    maas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sehir = models.CharField(max_length=100, default='Girilmedi')
    dogumtarihi = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.calisanid} - {self.isim} {self.soyisim} - {self.mail}'
    
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'
    