# Generated by Django 2.1.7 on 2019-03-14 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubuser',
            name='name',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
