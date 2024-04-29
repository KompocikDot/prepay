# Generated by Django 5.0.3 on 2024-04-26 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_payment_end_user_alter_payment_issuer'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Created'), ('WAITING_FOR_STRIPE_CONFIRMATION', 'Waiting For Stripe Confirmation'), ('CONFIRMED', 'Confirmed')], default='CREATED'),
        ),
    ]