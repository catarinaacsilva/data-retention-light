import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from influxdb_client import InfluxDBClient
from django.db import transaction
from django.conf import settings
from .models import Stay_Data, User, Receipt

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
    Receive data stay from cassiopeia
'''
@csrf_exempt
@api_view(('POST',))
def stayData(request):
    try:
        parameters = json.loads(request.body)
        datein = parameters['start_date']
        dateout = parameters['end_date']
        email = parameters['userid']
        receipt = parameters['receipt']

        #email = receipt['subjectEmail']

        # check if it exists
        qs = Stay_Data.objects.filter(email=email, datein=datein, dateout=dateout)
        if not qs.exists():
            with transaction.atomic():
                if not User.objects.filter(email=email).exists():
                    User.objects.create(email=email)
                user = User.objects.get(email=email)
                stay = Stay_Data.objects.create(email=user, datein=datein, dateout=dateout, data=True, receipt=receipt, receiptid=receipt['consentReceiptID'])

        else:
            stay = qs.first()

    except Exception as e:
        return Response(f'Exception: {e}\n', status=status.HTTP_400_BAD_REQUEST)
    
    print({'stay_id': stay.pk})
    return JsonResponse({'stay_id': int(stay.pk)}, status=status.HTTP_201_CREATED)


'''
    Remove user data of the influxdb by stay and the email
'''
@csrf_exempt
@api_view(('GET',))
def removeDataUser(request):
    try:
        token = request.GET['token']
        email = request.GET['userid']
        receiptid = request.GET['receipt_id']

        if token == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email=email)
        qs = Stay_Data.objects.filter(email=user, receiptid=receipt_id)

        dateIn = qs.datein
        dateOut = qs.dateout

        #check if dateIn and dateOut are Date
        if isinstance(dateIn, datetime.date):
            print('convert dateIn to datetime')
            dateIn = datetime.datetime(year=dateIn.year, month=dateIn.month, day=dateIn.day)

        if isinstance(dateOut, datetime.date):
            print('convert dateOut to datetime')
            dateOut = datetime.datetime(year=dateOut.year, month=dateOut.month, day=dateOut.day)
        fmt = '%Y-%m-%dT%H:%M:%SZ'
        #utc = pytz.utc
        #dateIn = utc.localize(dateIn)
        dateIn = dateIn.strftime(fmt)
        dateOut = dateOut.strftime(fmt) 

        print(f'In {dateIn} Out {dateOut}')
        
        #query = f'influx delete --bucket cassiopeiainflux --start {dateIn} --stop {dateOut}'
        client = get_influxdb_client()
        client.delete_api().delete(dateIn, dateOut, '',  bucket='cassiopeiainflux', org='it')
       
        #qs.update(data=False)
        qs.data = False
        qs.save()

        timestamp = datetime.timestamp(now)
        Receipt.objects.create(email=user, timestamp=timestamp)
        
    except Exception as e:
        return Response(f'Exception: {e}\n', status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)



'''
    Validate data deletion
'''
@csrf_exempt
@api_view(('GET',))
def cleanData(request):
    try:
        token = request.GET['token']
        email = request.GET['userid']
        receiptid = request.GET['receipt_id']

        if token == None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email=email)
        qs = Stay_Data.objects.filter(email=user, receiptid=receipt_id)

        receiptInfo = Receipt.get(email=user)
        
        if qs.data == True:
            return JsonResponse({
                'start_date': qs.datein,
                'end_date': qs.dateout,
                'email': email,
                'timestamp': receiptInfo.timestamp,
                'receiptDeletionId': receiptInfo.id,
                'Data': 'Not Removed'
                })
        else:
            return JsonResponse({
                'start_date': qs.datein,
                'end_date': qs.dateout,
                'email': email,
                'timestamp': receiptInfo.timestamp,
                'receiptDeletionId': receiptInfo.id,
                'Data': 'Removed'
                })

    except Exception as e:
        return Response(f'Exception: {e}\n', status=status.HTTP_400_BAD_REQUEST)

    