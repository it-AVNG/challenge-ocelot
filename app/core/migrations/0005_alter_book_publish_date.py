# Generated by Django 4.2.7 on 2023-11-17 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_book_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(blank=True, help_text='format: YYYY-MM-DD'),
        ),
    ]
