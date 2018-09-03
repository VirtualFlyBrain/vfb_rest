from django.db import models


PROJECT_CHOICES = [
       ('LC', 'L1EM_Cardona'),
       ('F', 'FAFB')]

class neuron(models.Model):
    vfbid = models.URLField(primary_key=True)
    primary_name = models.CharField(max_length=200, blank=False, help_text='The primary name for the individual neuron.')
    neuron_type = models.URLField(default='http://purl.obolibrary.org/obo/FBbt_00005106', blank=False,
                                      help_text='Valid VFB Identifier denoting anatomical entity, such as a neuron. If left blank, we will assign the default Neuron.')
    alternative_names = models.CharField(max_length=1000,
                                      help_text='Tube (|) seperated list of alternative terms (i.e. synonyms).')
    external_identifiers = models.CharField(max_length=1000,
                                      help_text='A unique identifier for the neuron in an external resource. E.g. CATMAID SKID or neuronID.  Where that external resource has multiple possible identifiers for the neuron, identifier string needs to make this clear. For CATMAID IDs please use SKID_nnnnnn or NeuronID_nnnnnn.')
    orcid = models.URLField(help_text='Valid orcid, i.e. https://orcid.org/0000-0000-0000-0000')
    datasetid = models.URLField(help_text='Valid dataset identifier, i.e. IRI. Must already be known to VFB knowledge base.')
    project = models.CharField(choices=PROJECT_CHOICES,max_length=200, blank=False, help_text= 'A valid name for a project.')
    classification_comment = models.CharField(max_length=1000,
                                              help_text='Comment on classification of neuron.')
    created = models.BooleanField()


    def __str__(self):
        return self.vfbid

    class Meta:
        ordering = ('vfbid',)

class dataset(models.Model):
    datasetid = models.URLField(primary_key=True)
    label = models.CharField(max_length=200, help_text='Short human-readable name for dataset.')
    short_form = models.CharField(max_length=50, help_text='Short id for dataset. No special characters or spaces.')
    created = models.BooleanField()

    def __str__(self):
        return self.datasetid

    class Meta:
        ordering = ('datasetid',)

class neuronSimple(models.Model):
    primary_name = models.CharField(max_length=200, blank=False, help_text='The primary name for the individual neuron.')
    neuron_type = models.URLField(default='http://purl.obolibrary.org/obo/FBbt_00005106', blank=False,
                                  help_text='Valid VFB Identifier denoting anatomical entity, such as a neuron. If left blank, we will assign the default Neuron.')
    alternative_names = models.CharField(max_length=1000,
                                         help_text='Comma seperated list of alternative terms (i.e. synonyms).')
    external_identifiers = models.CharField(max_length=1000,
                                            help_text='A unique identifier for the neuron in an external resource. E.g. CATMAID SKID or neuronID.  Where that external resource has multiple possible identifiers for the neuron, identifier string needs to make this clear. For CATMAID IDs please use SKID_nnnnnn or NeuronID_nnnnnn.')
    orcid = models.URLField(help_text='Valid orcid, i.e. https://orcid.org/0000-0000-0000-0000')
    datasetid = models.URLField(
        help_text='Valid dataset identifier, i.e. IRI. Must already be known to VFB knowledge base.')
    project = models.CharField(choices=PROJECT_CHOICES, max_length=200, blank=False,
                               help_text='A valid name for a project.')
    classification_comment = models.CharField(max_length=1000,
                                              help_text='Comment on classification of neuron.')

    def __str__(self):
        return self.primary_name

    class Meta:
        ordering = ('primary_name',)

class datasetSimple(models.Model):
    label = models.CharField(max_length=200, help_text='Short human-readable name for dataset.')
    short_form = models.CharField(max_length=50, help_text='Short id for dataset. No special characters or spaces.')

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('label',)


class person(models.Model):
    orcid = models.URLField(primary_key=True)

    def __str__(self):
        return self.orcid

    class Meta:
        ordering = ('orcid',)