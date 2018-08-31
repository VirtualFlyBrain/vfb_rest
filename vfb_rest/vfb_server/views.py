from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, viewsets
from .neo import neo
from .models import neuron, dataset
from .serializers import neuronSerializer, datasetSerializer, neuronSerializerSimple, datasetSerializerSimple

from django.db.utils import OperationalError

try:
    print('test')
except OperationalError:
    pass  # happens when db doesn't exist yet, views.py should be
          # importable without this side effect

class datasetViewSet(viewsets.ModelViewSet):
    queryset = dataset.objects.all()
    serializer_class = datasetSerializerSimple
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['post', 'head']

    def create(self, request, *args, **kwargs):
        # This is the main point: transforming the simple, user facing data model into the extended internal one
        data = self.create_or_get_dataset(data=request.data)
        print(data)
        serializer=datasetSerializer(data=data)
        #serializerSimple = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except Exception:
            print('Error: Validation of dataset failed during creation (datasetViewSet:create)')

        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def create_or_get_dataset(self,data):
        kb = neo()
        data = kb.create_or_get_dataset(name=data['label'],license='',short_form=data['short_form'],description='')
        return data

class neuronViewSet(viewsets.ModelViewSet):
    #authentication_classes = (authentication.TokenAuthentication,)
    queryset = neuron.objects.all()
    serializer_class = neuronSerializerSimple
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['post', 'head']

    def create(self, request, *args, **kwargs):
        data = self.create_or_get_neuron(data=request.data)
        serializer = neuronSerializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except:
            print('Error: Validation of neuron failed during creation (neuronViewSet:create)')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def create_or_get_neuron(self, data):
        kb = neo()
        data = kb.create_or_get_neuron(primary_name=data['primary_name'], alternative_names=data['alternative_names'], external_identifiers=data['external_identifiers'], orcid=data['orcid'], datasetid=data['datasetid'], anatomical_type=data['neuron_type'])
        return data

# @api_view(['GET', 'POST'])
# def requestId(request):
#     if request.method == 'POST':
#         kb = neo()
#         q = 'MATCH (n:DataSet) RETURN n'
#         result = kb.nc.commit_list([q])
#         if result:
#             dc = results_2_dict_list(result)
#             return Response(dc)
#     return Response({"message": "Hello, world!"})