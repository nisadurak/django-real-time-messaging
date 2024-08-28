import csv
from django.core.management.base import BaseCommand
from calisanlar.models import Calisan
from datetime import datetime

class Command(BaseCommand):
    help = 'Load data from Turkish Employee Dataset'

    def handle(self, *args, **kwargs):
        # Türkçe ay isimlerini İngilizce ay isimlerine çeviren sözlük
        ay_cevir = {
            "Ocak": "January", "Şubat": "February", "Mart": "March",
            "Nisan": "April", "Mayıs": "May", "Haziran": "June",
            "Temmuz": "July", "Ağustos": "August", "Eylül": "September",
            "Ekim": "October", "Kasım": "November", "Aralık": "December"
        }
        
        with open('calisanlar/data/calisan_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Türkçe ay adını İngilizceye çevir
                for turkce_ay, ingilizce_ay in ay_cevir.items():
                    if turkce_ay in row['DogumTarihi']:
                        row['DogumTarihi'] = row['DogumTarihi'].replace(turkce_ay, ingilizce_ay)
                        break
                
                # Tarihi uygun formata çevir
                dogumtarihi = datetime.strptime(row['DogumTarihi'], "%d %B %Y").date()
                
                # Veritabanına kaydet
                Calisan.objects.create(
                    calisanid=row['calisanid'],
                    isim=row['Isimler'],
                    soyisim=row['Soyisimler'],
                    telefonturu=row['TelefonTuru'],
                    telefon=row['Telefon'],
                    mail=row['mail'],
                    departman=row['Departman'],
                    maas=row['Maas'],
                    sehir=row['Sehir'],
                    dogumtarihi=dogumtarihi
                )
