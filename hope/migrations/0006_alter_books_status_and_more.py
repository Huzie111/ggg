# Generated by Django 4.0.5 on 2022-07-10 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hope', '0005_alter_borrowed_books_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='status',
            field=models.CharField(choices=[('AV', 'Available'), ('UNAV', 'Unavailable')], default='AV', max_length=20),
        ),
        migrations.AlterField(
            model_name='borrowed_books',
            name='return_status',
            field=models.CharField(choices=[('BK', 'Booked'), ('TK', 'Taken'), ('RT', 'Returned')], default='BK', max_length=15),
        ),
    ]