# Generated by Django 3.1.2 on 2020-10-01 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_app', '0013_auto_20201001_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='issued_by',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]