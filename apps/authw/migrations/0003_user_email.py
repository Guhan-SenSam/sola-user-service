# Generated by Django 5.1.5 on 2025-01-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authw', '0002_remove_user_email_user_privy_wallet_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True),
        ),
    ]
