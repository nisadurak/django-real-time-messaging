# Generated by Django 4.2.15 on 2024-08-24 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calisanlar', '0003_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calisan',
            name='mail',
            field=models.EmailField(default='example@example.com', max_length=254, unique=True, verbose_name='mail'),
        ),
    ]
