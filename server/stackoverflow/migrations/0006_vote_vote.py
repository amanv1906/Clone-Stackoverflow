# Generated by Django 2.2.17 on 2021-01-05 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stackoverflow', '0005_auto_20210105_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='vote',
            field=models.IntegerField(default=1),
        ),
    ]
