# Generated by Django 4.0.5 on 2022-07-10 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hope', '0003_borrowed_books_return_status_alter_books_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='status',
            field=models.CharField(choices=[('AV', 'Available'), ('UNAV', 'Unavailable')], default='Available', max_length=20),
        ),
        migrations.AlterField(
            model_name='borrowed_books',
            name='return_status',
            field=models.CharField(choices=[('BK', 'Booked'), ('TK', 'Taken'), ('RT', 'Returned')], default='Booked', max_length=15),
        ),
    ]