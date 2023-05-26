# Generated by Django 4.2.1 on 2023-05-26 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='')),
                ('about_org', models.TextField(max_length=500)),
                ('org_website', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Posting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=1000)),
                ('posted_on', models.DateField()),
                ('last_updated_on', models.DateField()),
                ('posting_url', models.URLField(max_length=300)),
                ('contact_details', models.CharField(max_length=250)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skillsapp.organization')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PostingSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skillsapp.posting')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skillsapp.skill')),
            ],
        ),
    ]