# Generated by Django 5.0.3 on 2024-05-03 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_stripe_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='stripe_account_id',
            field=models.UUIDField(null=True),
        ),
    ]
