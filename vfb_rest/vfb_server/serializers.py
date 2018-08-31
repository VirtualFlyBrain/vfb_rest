from rest_framework import serializers
from .models import neuron, dataset, neuronSimple, datasetSimple


class neuronSerializer(serializers.ModelSerializer):

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
