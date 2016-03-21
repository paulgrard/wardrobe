# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-19 15:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dressingManage', '0030_outfit_theme'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outfit',
            old_name='clothes',
            new_name='various',
        ),
        migrations.AddField(
            model_name='outfit',
            name='coat',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coat_outfit', to='dressingManage.Clothe'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='pant',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pant_outfit', to='dressingManage.Clothe'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='shoes',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shoes_outfit', to='dressingManage.Clothe'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='sock',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sock', to='dressingManage.Clothe'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='underwear',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='underwear_outfit', to='dressingManage.Clothe'),
        ),
        migrations.AddField(
            model_name='outfit',
            name='underwearTop',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='underwearTop_outfit', to='dressingManage.Clothe'),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='firstLayer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='firstLayer_outfit', to='dressingManage.Clothe'),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='secondLayer',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondLayer_outfit', to='dressingManage.Clothe'),
        ),
    ]
