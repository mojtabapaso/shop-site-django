# Generated by Django 4.1.3 on 2022-12-06 14:53

from django.db import migrations, models
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=250, unique=True, verbose_name='ایمیل')),
                ('phone_number', models.CharField(max_length=11, unique=True, verbose_name='شماره تلفن')),
                ('first_name', models.CharField(max_length=150, verbose_name='اسم')),
                ('last_name', models.CharField(max_length=150, verbose_name='فامیلی')),
                ('date_of_birth', django_jalali.db.models.jDateField(null=True, verbose_name='تاریخ تولد')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال')),
                ('is_admin', models.BooleanField(default=False, verbose_name='مدیر')),
                ('last_login', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='آخرین بازدید')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('code', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'کد ارسالی',
                'verbose_name_plural': 'کدهای ارسالی',
            },
        ),
    ]