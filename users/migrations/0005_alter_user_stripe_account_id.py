# Generated by Django 5.0.3 on 2024-05-06 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_stripe_account_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='stripe_account_id',
            field=models.CharField(null=True),
        ),
    ]
