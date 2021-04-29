import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from influxdb_client import InfluxDBClient
from django.conf import settings
from .models import Stay

'''
    Returns an ``InfluxDBClient`` instance.
'''
def get_influxdb_client():
    client = InfluxDBClient(
        url = settings.INFLUXDB_URL,
        token = settings.INFLUXDB_TOKEN,
        org = settings.INFLUXDB_ORG)
    return client


'''
    Remove data
'''
@csrf_exempt
@api_view(('POST',))
def removeData(request):
    try:
        parameters = json.loads(request.body)
        start_date = parameters['start_date']
        end_date = parameters['end_date']
        stay_id = parameters['stay_id']
        receipts = parameters['receipts']

        qs = Stay.objects.filter(stay_id=stay_id)

        if not qs.exists():
            dateIn = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            dateOut = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            fmt = '%Y-%m-%dT%H:%M:%SZ'
            #utc = pytz.utc
            #dateIn = utc.localize(dateIn)
            dateIn = dateIn.strftime(fmt)
            dateOut = dateOut.strftime(fmt) 

            print(f'In {dateIn} Out {dateOut}')
            
            #query = f'influx delete --bucket cassiopeiainflux --start {dateIn} --stop {dateOut}'
            client = get_influxdb_client()
            client.delete_api().delete(dateIn, dateOut, '',  bucket='cassiopeiainflux', org='it')

            Stay.objects.create(stay_id=stay_id, start_date=start_date, end_date=end_date, receipts=receipts)

    except Exception as e:
        return Response(f'Exception: {e}\n', status=status.HTTP_400_BAD_REQUEST)

    return Response('Data Removed', status=status.HTTP_200_OK)



'''
    Validate data deletion
'''
@csrf_exempt
@api_view(('GET',))
def cleanData(request):
    try:
        parameters = json.loads(request.body)
        dateIn = parameters['start_date']
        dateOut = parameters['end_date']
        stay_id = parameters['stay_id']
        receipts = parameters['receipts']

        qs = Stay.objects.filter(stay_id=stay_id)

        if qs.exists():
            return JsonResponse({'clean': True})
        else:
            return JsonResponse({'clean': False})

    except Exception as e:
        return Response(f'Exception: {e}\n', status=status.HTTP_400_BAD_REQUEST)

    