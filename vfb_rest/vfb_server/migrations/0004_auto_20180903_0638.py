# Generated by Django 2.1 on 2018-09-03 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vfb_server', '0003_auto_20180903_0629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neuron',
            name='primary_name',
            field=models.CharField(help_text='The primary name for the individual neuron.', max_length=200),
        ),
        migrations.AlterField(
            model_name='neuronsimple',
            name='primary_name',
            field=models.CharField(help_text='The primary name for the individual neuron.', max_length=200),
        ),
    ]
