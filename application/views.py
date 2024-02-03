import json

import numpy as np
import pandas as pd
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from application.models import Service, ServiceProvider, Branch, CustomerWaitingTime
from application.utils import calculate_waiting_time


# Create your views here.




@api_view(['GET'])
def get_all_services(request,category):
    if request.method =='GET':
        branches = Branch.objects.filter(category=category).all()
        services = Service.objects.filter(serviceserviceprovider__service_provider__branch_id__in=branches)
        return Response(services.values().distinct())

@api_view(['GET'])
def get_waiting_time(request,service_id):
    # last_frame = 140
    # customer_waiting_time = CustomerWaitingTime.objects.filter(last_updated__gt=last_frame,updatable=False,service_provider__serviceserviceprovider__service_id=service_id).values('service_provider_id','start_date','end_date')
    # dataframe = pd.DataFrame(customer_waiting_time)
    # dataframe['waiting_time'] = customer_waiting_time['start_date'] - customer_waiting_time['last_updated']
    return_value = [20,10,5]
    service_provider = ServiceProvider.objects.filter(serviceserviceprovider__service_id=service_id)
    return_objective =[]
    for service in service_provider.values():
        service['waiting_time'] = np.random.randint(1,30)
        return_objective.append(service)
    # for i, group in dataframe.groupby('service_provider_id'):
    #     return_value.append({i:np.average(group['waiting_time'])})
    return_value = [{"service_provider_id":3,"waiting_time":20},{"service_provider_id":4,"waiting_time":14},{"service_provider_id":7,"waiting_time":35},{"service_provider_id":8,"waiting_time":5}]
    return Response(return_objective)

@api_view(['GET'])
def get_service_providers(request,service_provider_id):
    service_provider = ServiceProvider.objects.get(service_provider_id=service_provider_id)
    return Response(service_provider.values())

@api_view(['GET'])
def get_all_service_providers(request):
    service_provider = ServiceProvider.objects.all()
    return Response(service_provider.values())

@api_view(['GET'])
def get_provider_waiting_time(request,last_frame,service_provider):
    # CustomerWaitingTime.objects.all().delete()
    # calculate_waiting_time(service_provider_id=1)
    customer_waiting_time = CustomerWaitingTime.objects.filter(updatable=False,
                                                               service_provider_id=service_provider).values(
        'service_provider_id', 'start_date', 'last_updated')
    dataframe = pd.DataFrame(customer_waiting_time)
    dataframe['waiting_time'] = dataframe['last_updated'] -dataframe['start_date']
    # dataframe = dataframe[dataframe['waiting_time'] >5]
    # dataframe = dataframe[dataframe['waiting_time'] < 1800]
    five = dataframe['waiting_time'].rolling(500).mean()
    ten = dataframe['waiting_time'].rolling(1000).mean()
    fiftheen = dataframe['waiting_time'].rolling(1500).mean()
    return_value = {"service_provider":service_provider,"waiting_time": np.average(dataframe['waiting_time']),"five":np.mean(five),"ten":np.mean(ten),"fiftheen":np.mean(fiftheen)}
    return Response(return_value)






