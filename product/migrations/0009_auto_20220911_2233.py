# Generated by Django 3.2.9 on 2022-09-11 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20220911_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='size1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
