# Generated by Django 5.0.3 on 2024-03-25 13:57

import django.db.models.deletion
import djmoney.models.fields
import djmoney.models.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('USD', 'USD $'), ('EUR', 'EUR €'), ('PLN', 'PLN zł')], default=None, editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(currency_choices=[('USD', 'USD $'), ('EUR', 'EUR €'), ('PLN', 'PLN zł')], decimal_places=2, max_digits=7, validators=[djmoney.models.validators.MinMoneyValidator({'EUR': 1, 'PLN': 5, 'USD': 1}), djmoney.models.validators.MaxMoneyValidator({'EUR': 20000, 'PLN': 99999, 'USD': 20000})])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('end_user', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='end_user', to=settings.AUTH_USER_MODEL)),
                ('issuer', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='issuer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
