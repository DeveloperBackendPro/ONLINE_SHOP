# Generated by Django 5.0.1 on 2024-02-12 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_news_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='short_description_en',
            field=models.TextField(null=True, verbose_name='Краткое описание'),
        ),
        migrations.AddField(
            model_name='news',
            name='short_description_ru',
            field=models.TextField(null=True, verbose_name='Краткое описание'),
        ),
        migrations.AddField(
            model_name='news',
            name='short_description_uz',
            field=models.TextField(null=True, verbose_name='Краткое описание'),
        ),
    ]