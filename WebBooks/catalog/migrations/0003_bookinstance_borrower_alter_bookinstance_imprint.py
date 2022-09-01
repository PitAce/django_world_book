# Generated by Django 4.1 on 2022-08-21 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0002_alter_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(blank=True, help_text='Выберите заказчика книги', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Заказчик'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='imprint',
            field=models.CharField(help_text='Введите издательство и год выпуска', max_length=20, verbose_name='Издательств_OGOG'),
        ),
    ]
