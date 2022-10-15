# Generated by Django 3.2.9 on 2022-10-15 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_alter_productimage_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description_ar',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='description'),
        ),
        migrations.AddField(
            model_name='product',
            name='details_ar',
            field=models.TextField(blank=True, null=True, verbose_name='details'),
        ),
        migrations.AddField(
            model_name='product',
            name='details_en',
            field=models.TextField(blank=True, null=True, verbose_name='details'),
        ),
        migrations.AddField(
            model_name='product',
            name='name_ar',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='product',
            name='name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='name'),
        ),
    ]
