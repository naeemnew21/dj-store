# Generated by Django 3.2.9 on 2022-10-04 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20221004_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='add1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='add2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]