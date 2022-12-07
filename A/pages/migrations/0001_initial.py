# Generated by Django 4.1.3 on 2022-12-06 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sub_category', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scategory', to='pages.category')),
            ],
            options={
                'verbose_name': 'طبقه بندی',
                'verbose_name_plural': 'طبقه بندی ها',
                'ordering': ('name',),
            },
        ),
    ]