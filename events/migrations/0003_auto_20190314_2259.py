# Generated by Django 2.1.7 on 2019-03-14 22:59

from django.db import migrations, models


def id_to_event_id(apps, schema_editor):
    Event = apps.get_model('events', 'Event')
    for event in Event.objects.all():
        event.event_id = event.id
        event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20190224_0129'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RunPython(id_to_event_id),
    ]
