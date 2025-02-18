# Generated by Django 5.1.6 on 2025-02-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_borrower', models.CharField(max_length=100)),
                ('email_of_borrower', models.EmailField(max_length=254)),
                ('time_of_transaction', models.DateTimeField(auto_now_add=True)),
                ('time_of_return', models.DateTimeField(null=True)),
                ('returned', models.BooleanField(default=False)),
                ('remarks', models.TextField()),
            ],
        ),
    ]
