from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import authentication, permissions, status, viewsets
from .neo import neo
from .models import neuron, dataset, person
from .serializers import neuronSerializer, datasetSerializer, neuronSerializerSimple, datasetSerializerSimple, \
    personSerializer

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
        message = ''
        created = False


        try:
            data = self.create_or_get_dataset(data=request.data)
            serializer = datasetSerializer(data=data)
            created = data['created']
            # serializerSimple = self.get_serializer(data=data)
            try:
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            except:
                pass
        except Exception as e:
            print('Error: Validation of dataset failed during creation (datasetViewSet:create): '+str(e))
            message = str(e)

        if message =='':
            d = serializer.data
            headers = self.get_success_headers(d)
            response = dict()
            if created is False:
                response['data'] = d
                response['message'] = "A dataset with the given short_form was already created. Return existing record."
                print("Response: " + str(response))
                return Response("{message: " + str(response) + "}", status=status.HTTP_202_ACCEPTED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response("{message: " + message + "}", status=status.HTTP_404_NOT_FOUND)

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
        message = ''
        created = False
        neuron = request.data['primary_name']
        dataset  = request.data['datasetid']

        try:
            data = self.create_or_get_neuron(data=request.data)
            created = data['created']
            serializer = neuronSerializer(data=data)
            try:
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            except:
                pass
        except Exception as e:
            print(e)
            message = str(e)

        if message =='':
            #d = serializer.data
            #headers = self.get_success_headers(d)
            #response = dict()
            if created is False:
                # response['data'] = d
                # response['message'] = "A neuron with label " + neuron + " was already registered for the dataset " + dataset + ". Return existing record."
                # print("Response: " + str(response))
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response("{message: " + message + "}", status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save()

    def create_or_get_neuron(self, data):
        kb = neo()
        data = kb.create_or_get_neuron(primary_name=data['primary_name'], alternative_names=data['alternative_names'], external_identifier=data['external_identifiers'], classification_comment=data['classification_comment'], orcid=data['orcid'], project=data['project'], datasetid=data['datasetid'], anatomical_type=data['neuron_type'])
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

class personViewSet(viewsets.ModelViewSet):
    queryset = person.objects.all()
    serializer_class = personSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    http_method_names = ['post', 'head']

    def create(self, request, *args, **kwargs):
        # This is the main point: transforming the simple, user facing data model into the extended internal one

        message = ''
        created = False

        try:
            data = self.create_or_get_person(data=request.data)
            created = data['created']
            serializer = self.get_serializer(data=data)
            try:
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            except:
                pass

        except Exception as e:
            print(e)
            message = str(e)

        if message =='':
            d = serializer.data
            headers = self.get_success_headers(d)
            response = dict()
            if created is False:
                response['data'] = d
                response['message'] = "Person was already created.."
                print("Response: "+str(response))
                return Response(data=str(response), status=status.HTTP_304_NOT_MODIFIED, headers=headers)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response("{message: " + message + "}", status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        serializer.save()

    def create_or_get_person(self,data):
        kb = neo()
        data = kb.create_or_get_person(orcid=data['orcid'])
        return data
