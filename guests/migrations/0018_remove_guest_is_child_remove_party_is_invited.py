# Generated by Django 4.0.1 on 2022-01-28 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0017_remove_guest_email_remove_party_invitation_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='is_child',
        ),
        migrations.RemoveField(
            model_name='party',
            name='is_invited',
        ),
    ]
