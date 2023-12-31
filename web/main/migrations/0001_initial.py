# Generated by Django 3.2.18 on 2023-05-23 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perfume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('image_url', models.TextField()),
                ('accords', models.TextField()),
                ('notes', models.TextField()),
                ('average_rating', models.TextField()),
                ('ratings_count', models.TextField()),
                ('weighted_rating', models.TextField()),
                ('date', models.TextField()),
                ('longevity', models.TextField()),
                ('season', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('likes', models.TextField()),
                ('dislike', models.TextField()),
            ],
        ),
    ]
