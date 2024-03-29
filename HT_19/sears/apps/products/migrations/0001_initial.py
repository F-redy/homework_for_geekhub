# Generated by Django 5.0 on 2024-01-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('brand', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('image_url', models.TextField(blank=True)),
                ('base_price', models.FloatField()),
                ('final_price', models.FloatField()),
                ('savings_price', models.FloatField(default=0.0)),
                ('url', models.URLField(blank=True)),
                ('short_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
