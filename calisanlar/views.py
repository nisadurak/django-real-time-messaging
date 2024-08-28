from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import RegistrationForm
from .models import Calisan
from .models import Message
from django.db.models import F, ExpressionWrapper, IntegerField, Count, Q
from datetime import date
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, IntegerField, ExpressionWrapper


def register(request):
    """Kullanıcı kayıt görünümü."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Kullanıcıyı henüz kaydetme
            user.is_active = True  # Kullanıcıyı aktif olarak işaretle
            user.save()  # Kullanıcıyı kaydet
            login(request, user)
            messages.success(request, 'Kayıt başarılı! Sohbet odasına yönlendiriliyorsunuz.')
            return redirect('room', room_name='general')
        else:
            messages.error(request, 'Kayıt sırasında bir hata oluştu. Lütfen tekrar deneyin.')
    else:
        form = RegistrationForm()
    return render(request, 'calisanlar/register.html', {'form': form})

def login_view(request):
    """Kullanıcı giriş görünümü."""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Başarıyla giriş yaptınız!')
            return redirect('room', room_name='general')
        else:
            messages.error(request, 'Giriş başarısız. Lütfen bilgilerinizi kontrol edip tekrar deneyin.')
    else:
        form = AuthenticationForm()
    return render(request, 'calisanlar/login.html', {'form': form})

@login_required
def room(request, room_name):
    """Sohbet odası görünümü."""
    messages = Message.objects.filter(room=room_name).order_by('timestamp')  # Mesajları odaya göre filtrele ve sırala
    return render(request, 'calisanlar/room.html', {'room_name': room_name, 'messages': messages
        
    })

@login_required
def dashboard(request):
    """Dashboard görünümü - Departman, şehir, yaş ve maaşa göre çalışan sayısını gösterir."""
    departman_verileri = Calisan.objects.values('departman').annotate(sayi=Count('calisanid')).order_by('-sayi')
    sehir_verileri = Calisan.objects.values('sehir').annotate(sayi=Count('calisanid')).order_by('-sayi')
    
    # Şu anki tarih ve yaş hesaplaması
    current_date = date.today()
    yas_verileri = Calisan.objects.annotate(
        yas=ExpressionWrapper((current_date.year - F('dogumtarihi__year')), output_field=IntegerField())
    ).values('yas').annotate(sayi=Count('calisanid')).order_by('yas')

    # Yaş kategorilerine göre gruplama
    yas_kategorileri = [
        {'kategori': '18 yaş altı', 'sayi': yas_verileri.filter(yas__lt=18).count()},
        {'kategori': '18-25', 'sayi': yas_verileri.filter(yas__gte=18, yas__lte=25).count()},
        {'kategori': '26-30', 'sayi': yas_verileri.filter(yas__gte=26, yas__lte=30).count()},
        {'kategori': '31-40', 'sayi': yas_verileri.filter(yas__gte=31, yas__lte=40).count()},
        {'kategori': '41-50', 'sayi': yas_verileri.filter(yas__gte=41, yas__lte=50).count()},
        {'kategori': '50 yaş üstü', 'sayi': yas_verileri.filter(yas__gt=50).count()},
    ]

    # Maaş kategorilerine göre gruplama
    maas_kategorileri = [
        {'kategori': '17,000 TL altı', 'sayi': Calisan.objects.filter(maas__lt=17000).count()},
        {'kategori': '17,000-21,000 TL', 'sayi': Calisan.objects.filter(maas__gte=17000, maas__lte=21000).count()},
        {'kategori': '21,001-30,000 TL', 'sayi': Calisan.objects.filter(maas__gte=21001, maas__lte=30000).count()},
        {'kategori': '30,001-40,000 TL', 'sayi': Calisan.objects.filter(maas__gte=30001, maas__lte=40000).count()},
        {'kategori': '40,001-50,000 TL', 'sayi': Calisan.objects.filter(maas__gte=40001, maas__lte=50000).count()},
        {'kategori': '50,001-60,000 TL', 'sayi': Calisan.objects.filter(maas__gte=50001, maas__lte=60000).count()},
        {'kategori': '60,000 TL üstü', 'sayi': Calisan.objects.filter(maas__gt=60000).count()},
    ]

    context = {
        'departman_verileri': list(departman_verileri),
        'sehir_verileri': list(sehir_verileri),
        'yas_verileri': yas_kategorileri,
        'maas_verileri': maas_kategorileri,
    }

    return render(request, 'calisanlar/dashboard.html', context)