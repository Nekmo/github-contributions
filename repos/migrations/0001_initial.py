# Generated by Django 2.1.7 on 2019-02-24 01:29

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('owner', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=255)),
                ('private', models.BooleanField()),
                ('description', models.TextField(blank=True)),
                ('default_branch', models.CharField(default='master', max_length=100)),
                ('fork', models.BooleanField()),
                ('homepage', models.URLField(blank=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('has_issues', models.BooleanField()),
                ('has_projects', models.BooleanField()),
                ('has_wiki', models.BooleanField()),
                ('has_pages', models.BooleanField()),
                ('has_downloads', models.BooleanField()),
                ('archived', models.BooleanField()),
                ('mirror_url', models.URLField(blank=True)),
                ('data', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
    ]
