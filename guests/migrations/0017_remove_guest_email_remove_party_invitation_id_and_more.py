# Generated by Django 4.0.1 on 2022-01-28 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0016_party_rehearsal_dinner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='email',
        ),
        migrations.RemoveField(
            model_name='party',
            name='invitation_id',
        ),
        migrations.RemoveField(
            model_name='party',
            name='invitation_opened',
        ),
        migrations.RemoveField(
            model_name='party',
            name='invitation_sent',
        ),
        migrations.RemoveField(
            model_name='party',
            name='save_the_date_opened',
        ),
        migrations.RemoveField(
            model_name='party',
            name='save_the_date_sent',
        ),
        migrations.AlterField(
            model_name='guest',
            name='meal',
            field=models.CharField(blank=True, choices=[('vegetarian', 'vegetarian'), ('vegan', 'vegan'), ('any', 'any')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='party',
            name='type',
            field=models.CharField(choices=[('marina_family', 'marina_family'), ('eric_family', 'eric_family'), ('marina_friend', 'marina_friend'), ('eric_friend', 'eric_friend')], max_length=13),
        ),
    ]
