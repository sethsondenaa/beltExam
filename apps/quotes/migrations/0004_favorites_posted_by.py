# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-03 02:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0003_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorites',
            name='posted_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='posted_by', to='quotes.User'),
            preserve_default=False,
        ),
    ]