# Generated by Django 4.2.7 on 2023-12-05 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newscategory',
            name='type',
            field=models.CharField(choices=[('Акции', 'Акции'), ('События', 'События'), ('Организация', 'Организация')], max_length=20, verbose_name='Тип новостей'),
        ),
    ]
