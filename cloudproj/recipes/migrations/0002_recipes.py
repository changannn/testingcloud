# Generated by Django 4.2.4 on 2023-10-27 04:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('cuisine', models.CharField(max_length=64)),
                ('time', models.PositiveIntegerField()),
                ('ingredients', models.JSONField()),
                ('steps', models.JSONField()),
                ('calories', models.PositiveIntegerField()),
                ('image', models.URLField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
