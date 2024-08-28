
# Django Gerçek Zamanlı Mesajlaşma Uygulaması

Bu proje, Django kullanarak gerçek zamanlı mesajlaşma sağlayan bir web uygulamasıdır. Uygulama, kullanıcı kaydı ve giriş işlemlerini destekler ancak bildirim göndermez. Mesajlaşma WebSocket üzerinden yapılır.

## Gereksinimler

- Python 3.x
- Django 4.x
- Redis
- Uvicorn (ASGI sunucusu)

## Kurulum

1. Gerekli bağımlılıkları yükleyin:

    ```bash
    pip install -r requirements.txt
    ```

2. Verilerinizi import edin: 

    ```bash
    python manage.py load_data
    ```

3. Veritabanını migrate edin:

    ```bash
    python manage.py makemigrations 
    python manage.py migrate 
    ```

4. Redis sunucusunu başlatın:

    ```bash
    redis-server 
    ```

   Redis'in çalışıp çalışmadığını kontrol edin:

    ```bash
    redis-cli ping
    ```

   `PONG` yanıtını görürseniz Redis düzgün çalışıyor demektir.

5. Ortam değişkenlerini ayarlayın:

   Uvicorn sunucusunu çalıştırmadan önce Django ayarlarını belirtmeniz gerekebilir. Ortam değişkenlerini aşağıdaki komutla ayarlayın:

    ```bash
    $env:DJANGO_SETTINGS_MODULE="calisan_projesi.settings"
    ```

6. Uygulamayı başlatın:

    ```bash
    uvicorn calisan_projesi.asgi:application --port 8000 
    ```

## Kullanım

- **Kullanıcı Kaydı:** Kullanıcılar web arayüzünden kayıt olabilir.
- **Giriş Yapma:** Mevcut kullanıcılar giriş yapabilir ve mesajlaşmaya başlayabilir.
- **Mesajlaşma:** Kullanıcılar gerçek zamanlı olarak mesaj gönderebilir ve alabilir.

## Veri Testi

Uygulama, veri tabanı içerisinde Türkçe karakterler içerebilir. Kullanıcılar test yaparken bu karakterleri değiştirip kayıt edebilir veya veriyi tamamen değiştirebilir.

## Yönetici Paneli

Yönetici paneline erişmek ve kayıt oluşturmak için aşağıdaki adımları izleyin:

1. **Admin Kullanıcısı Oluşturun:**

    ```bash
    python manage.py createsuperuser
    ```

2. **Yönetici Paneline Giriş Yapın:**

   Web tarayıcınızı açın ve `http://127.0.0.1:8000/admin/` adresine gidin. Buradan yönetici girişi yaparak yeni kayıtlar oluşturabilirsiniz.

3. **Oda Ekranlarını Görüntüleyin:**

   Mesajlaşma ekranlarını görüntülemek için `http://127.0.0.1:8000/room_name/` adresini kullanabilirsiniz. Django geliştirme sunucusunun varsayılan adresi `http://127.0.0.1:8000`'dir, ancak farklı bir port veya IP adresi kullanıyorsanız URL'yi buna göre ayarlayın.

## Katkıda Bulunanlar

- Nisa DURAK

# MERKALISI İÇİN :
# Django Projesi ile Celery Kullanımı

Bu proje, Celery kullanarak arka plan görevlerini yönetme yeteneğine sahiptir. Aşağıda Celery ve alternatif olarak Django Q ile ilgili yapılandırma adımları bulunmaktadır.

### A. Celery ile Arka Plan Görevlerinin Yönetimi

Celery, dağıtılmış iş kuyruklarını kullanarak Python'da arka plan işlemleri gerçekleştirmeye yarayan güçlü bir araçtır. Django ile entegre olarak çalışabilir ve veri güncelleme gibi işlemleri belirli aralıklarla otomatik olarak gerçekleştirebilir.

1. **Celery ve Gerekli Bağımlılıkların Kurulumu:**

    ```bash
    pip install celery redis
    ```

2. **Django Projesinde Celery Yapılandırması:**

   Ana proje dizininde `celery.py` adlı bir dosya oluşturun ve aşağıdaki kodları ekleyin:

    ```python
    from __future__ import absolute_import, unicode_literals
    import os
    from celery import Celery

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
    app = Celery('your_project_name')
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
    ```

3. **Celery'i Django Ayar Dosyası ile Entegre Etme:**

   `settings.py` dosyanıza Celery ile ilgili aşağıdaki ayarları ekleyin:

    ```python
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    ```

4. **Görev Oluşturma ve Zamanlama:**

   Arka plan işlemleri için Celery görevlerini tanımlayın. Örneğin, veritabanını güncelleyen bir görev:

    ```python
    from celery import shared_task
    from your_app.models import Calisan

    @shared_task
    def verileri_guncelle():
        print("Veriler güncelleniyor...")
    ```

5. **Celery Worker ve Beat Başlatma:**

    ```bash
    celery -A your_project_name worker -l info
    celery -A your_project_name beat -l info
    ```

### B. Django Q ile Alternatif Zamanlama

Django Q, Celery'ye alternatif olarak kullanılabilir. Aşağıdaki adımları izleyin:

1. **Django Q'nun Kurulumu:**

    ```bash
    pip install django-q
    ```

2. **Django Q Ayarları:**

   `settings.py` dosyanıza Django Q ile ilgili aşağıdaki ayarları ekleyin:

    ```python
    Q_CLUSTER = {
        'name': 'DjangoORM',
        'workers': 4,
        'recycle': 500,
        'timeout': 60,
        'django_redis': 'default',
        'queue_limit': 50,
        'bulk': 10,
        'orm': 'default',
    }
    ```

3. **Django Q Görev Tanımlaması ve Zamanlaması:**

   Bir görev tanımlamak ve zamanlamak için `tasks.py` dosyanıza aşağıdaki kodu ekleyin:

    ```python
    from django_q.tasks import schedule
    from django.utils import timezone
    from your_app.models import Calisan

    def verileri_guncelle():
        print("Veriler güncelleniyor...")

    schedule('your_app.tasks.verileri_guncelle',
             next_run=timezone.now(),
             schedule_type='H',
             repeats=-1)
    ```

--- 

