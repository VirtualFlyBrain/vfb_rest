# Generated by Django 2.1 on 2018-08-31 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dataset',
            fields=[
                ('datasetid', models.URLField(primary_key=True, serialize=False)),
                ('label', models.CharField(help_text='Short human-readable name for dataset.', max_length=200)),
                ('short_form', models.CharField(help_text='Short id for dataset. No special characters or spaces.', max_length=50)),
                ('created', models.BooleanField()),
            ],
            options={
                'ordering': ('datasetid',),
            },
        ),
        migrations.CreateModel(
            name='datasetSimple',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Short human-readable name for dataset.', max_length=200)),
                ('short_form', models.CharField(help_text='Short id for dataset. No special characters or spaces.', max_length=50)),
            ],
            options={
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='neuron',
            fields=[
                ('vfbid', models.URLField(primary_key=True, serialize=False)),
                ('primary_name', models.CharField(max_length=200)),
                ('anatomical_type', models.URLField(default='http://purl.obolibrary.org/obo/FBbt_00005106', help_text='Valid VFB Identifier denoting anatomical entity, such as a neuron. If left blank, we will assign the default Neuron.')),
                ('alternative_names', models.CharField(help_text='Comma seperated list of alternative terms (i.e. synonyms).', max_length=1000)),
                ('external_identifiers', models.CharField(help_text='External identifier, if exists.', max_length=1000)),
                ('orcid', models.URLField(help_text='Valid orcid, i.e. https://orcid.org/0000-0000-0000-0000')),
                ('datasetid', models.URLField(help_text='Valid dataset identifier, i.e. IRI. Must already be known to VFB knowledge base.')),
                ('created', models.BooleanField()),
            ],
            options={
                'ordering': ('vfbid',),
            },
        ),
        migrations.CreateModel(
            name='neuronSimple',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary_name', models.CharField(max_length=200)),
                ('neuron_type', models.URLField(default='http://purl.obolibrary.org/obo/FBbt_00005106', help_text='Valid VFB Identifier denoting anatomical entity, such as a neuron. If left blank, we will assign the default Neuron.')),
                ('alternative_names', models.CharField(help_text='Comma seperated list of alternative terms (i.e. synonyms).', max_length=1000)),
                ('external_identifiers', models.CharField(help_text='External identifier, if exists.', max_length=1000)),
                ('orcid', models.URLField(help_text='Valid orcid, i.e. https://orcid.org/0000-0000-0000-0000')),
                ('datasetid', models.URLField(help_text='Valid dataset identifier, i.e. IRI. Must already be known to VFB knowledge base.')),
            ],
            options={
                'ordering': ('primary_name',),
            },
        ),
    ]
