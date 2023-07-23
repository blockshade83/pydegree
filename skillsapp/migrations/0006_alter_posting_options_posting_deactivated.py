# Generated by Django 4.2.1 on 2023-07-22 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skillsapp', '0005_posting_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posting',
            options={'ordering': ['-last_updated_on']},
        ),
        migrations.AddField(
            model_name='posting',
            name='deactivated',
            field=models.BooleanField(default=False),
        ),
    ]