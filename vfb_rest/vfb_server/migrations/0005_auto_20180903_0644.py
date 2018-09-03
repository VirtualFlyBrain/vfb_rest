# Generated by Django 2.1 on 2018-09-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vfb_server', '0004_auto_20180903_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neuron',
            name='external_identifiers',
            field=models.CharField(help_text='A unique identifier for the neuron in an external resource. E.g. CATMAID SKID or neuronID.  Where that external resource has multiple possible identifiers for the neuron, identifier string needs to make this clear. For CATMAID IDs please use SKID_nnnnnn or NeuronID_nnnnnn.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='neuronsimple',
            name='external_identifiers',
            field=models.CharField(help_text='A unique identifier for the neuron in an external resource. E.g. CATMAID SKID or neuronID.  Where that external resource has multiple possible identifiers for the neuron, identifier string needs to make this clear. For CATMAID IDs please use SKID_nnnnnn or NeuronID_nnnnnn.', max_length=1000),
        ),
    ]
