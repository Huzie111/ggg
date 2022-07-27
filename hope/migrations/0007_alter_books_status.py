# Generated by Django 4.0.5 on 2022-07-10 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hope', '0006_alter_books_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='status',
            field=models.CharField(choices=[('AV', 'Available'), ('UNAV', 'Unavailable'), ('BK', 'Booked')], default='AV', max_length=20),
        ),
    ]
