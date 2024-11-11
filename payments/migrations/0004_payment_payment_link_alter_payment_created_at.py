# Generated by Django 5.1.2 on 2024-11-11 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_payment_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_link',
            field=models.URLField(blank=True, max_length=500, null=True, verbose_name='Ссылка на оплату'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты'),
        ),
    ]
