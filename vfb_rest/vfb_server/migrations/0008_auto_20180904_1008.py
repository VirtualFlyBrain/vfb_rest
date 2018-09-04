# Generated by Django 2.1 on 2018-09-04 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vfb_server', '0007_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='neuron',
            name='alternative_names',
            field=models.CharField(help_text='Tube (|) seperated list of alternative terms (i.e. synonyms). Example input: "Alt label 1|Alt label 2|Alt label 3".', max_length=1000),
        ),
        migrations.AlterField(
            model_name='neuron',
            name='datasetid',
            field=models.CharField(help_text='Valid dataset identifier, i.e. short form identifier. Must already be known to VFB knowledge base. To register, use dataset REST service. Example input: "Ito2013".', max_length=200),
        ),
        migrations.AlterField(
            model_name='neuron',
            name='neuron_type',
            field=models.CharField(default='FBbt_00005106', help_text='Valid VFB Identifier denoting anatomical entity, such as a neuron (FBbt_00005106). If left blank, we will assign the default FBbt_00005106 (Neuron).', max_length=200),
        ),
        migrations.AlterField(
            model_name='neuron',
            name='orcid',
            field=models.CharField(help_text='Please use your valid orcid, i.e. 0000-0000-0000-0001', max_length=200),
        ),
        migrations.AlterField(
            model_name='neuron',
            name='project',
            field=models.CharField(help_text='A valid name for a project, such as L1EM_Cardona or FAFB.', max_length=200),
        ),
        migrations.AlterField(
            model_name='neuronsimple',
            name='alternative_names',
            field=models.CharField(help_text='Tube (|) seperated list of alternative terms (i.e. synonyms). Example input: "Alt label 1|Alt label 2|Alt label 3".', max_length=1000),
        ),
        migrations.AlterField(
            model_name='neuronsimple',
            name='datasetid',
            field=models.CharField(help_text='Valid dataset identifier, i.e. short form identifier. Must already be known to VFB knowledge base. To register, use dataset REST service. Example input: "Ito2013".', max_length=200),
        ),
        migrations.AlterField(
            model_name='neuronsimple',
            name='neuron_type',
            field=models.CharField(default='FBbt_00005106', help_text='Valid VFB Identifier denoting anatomical entity, such as a neuron (FBbt_00005106). If left blank, we will assign the default FBbt_00005106 (Neuron).', max_length=200),
        ),
        migrations.AlterField(
            model_name='neuronsimple',
            name='orcid',
            field=models.CharField(help_text='Please use your valid orcid, i.e. 0000-0000-0000-0001', max_length=200),
        ),
        migrations.AlterField(
            model_name='neuronsimple',
            name='project',
            field=models.CharField(help_text='A valid name for a project, such as L1EM_Cardona or FAFB.', max_length=200),
        ),
    ]
