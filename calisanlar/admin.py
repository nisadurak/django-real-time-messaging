from django.contrib import admin
from .models import Message, Calisan  # Modelleri tek bir satırda import edin

@admin.register(Calisan)
class CalisanAdmin(admin.ModelAdmin):
    list_display = ('isim', 'soyisim', 'departman', 'sehir')
    search_fields = ('isim', 'soyisim', 'departman', 'sehir')

@admin.register(Message)  # Doğru dekoratörü kullanarak admin'e kaydedin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'content', 'timestamp')  # Görünmesini istediğiniz alanlar
    search_fields = ('user__username', 'room', 'content')  # Arama yapılacak alanlar
    list_filter = ('room', 'timestamp')  # Filtreleme için kullanılacak alanlar
