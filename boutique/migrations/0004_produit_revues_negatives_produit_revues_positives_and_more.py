# Generated by Django 4.0.1 on 2022-05-19 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boutique', '0003_produit_in_user_souhait'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='revues_negatives',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='produit',
            name='revues_positives',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='revue',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createur', to=settings.AUTH_USER_MODEL),
        ),
    ]
