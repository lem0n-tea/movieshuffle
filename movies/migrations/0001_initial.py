# Generated by Django 5.1.5 on 2025-02-13 08:32

import django.core.validators
import django.db.models.deletion
import django.db.models.functions.text
import movies.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a genre', max_length=200, unique=True)),
            ],
            options={
                'constraints': [models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='genre_name_case_insensitive_unique', violation_error_message='Genre already exists (case insensitive match)')],
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('imdb_id', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Enter a title', max_length=200)),
                ('description', models.TextField(blank=True, help_text='Enter a description', max_length=2000, null=True)),
                ('poster', models.ImageField(blank=True, null=True, upload_to=movies.models.poster_upload_path)),
                ('release_year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900)])),
                ('genres', models.ManyToManyField(to='movies.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movies', models.ManyToManyField(to='movies.movie')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
