from rest_framework import serializers
from .models import neuron, dataset, neuronSimple, datasetSimple, PROJECT_CHOICES, person


class neuronSerializer(serializers.ModelSerializer):
    project = serializers.ChoiceField(choices=PROJECT_CHOICES, default='L1EM_Cardona')
    class Meta:
        model=neuron
        fields='__all__'

class datasetSerializer(serializers.ModelSerializer):

    class Meta:
        model=dataset
        fields=('__all__')

class neuronSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = neuronSimple
        fields = '__all__'

class datasetSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = datasetSimple
        fields = ('__all__')

class personSerializer(serializers.ModelSerializer):
    class Meta:
        model = person
        fields = ('__all__')