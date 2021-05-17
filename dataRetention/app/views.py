import json
import datetime
import pytz
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from influxdb_client import InfluxDBClient
from django.db import transaction
from django.conf import settings
from .models import Stay_Data, Contact, Receipt
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@csrf_exempt
@api_view(('GET',))
def token(request):
    user = User.objects.get(username='privdash')

    if not user:
        user = User.objects.create_user('privdash', 'privdash@privdash.com', 'privdash')
        token = Token.objects.create(user=user)
    
    token = Token.objects.get(user=user)
    print(token.key)
    return JsonResponse({'token':str(token)})


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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def stayData(request):
    try:
        parameters = json.loads(request.body)
        datein = parameters['start_date']
        dateout = parameters['end_date']
        email = parameters['userid']
        receipt = parameters['receipt']

        date_format = '%Y-%m-%d %H:%M:%S'

        # convert to UTC timezone
        unaware_start_date = datetime.datetime.strptime(datein, date_format)
        aware_start_date = pytz.utc.localize(unaware_start_date)

        unaware_end_date = datetime.datetime.strptime(dateout, date_format)
        aware_end_date = pytz.utc.localize(unaware_end_date)

        #email = receipt['subjectEmail']

        # check if it exists
        qs = Stay_Data.objects.filter(email=email, datein=aware_start_date, dateout=aware_end_date)
        if not qs.exists():
            with transaction.atomic():
                if not Contact.objects.filter(email=email).exists():
                    Contact.objects.create(email=email)
                user = Contact.objects.get(email=email)
                stay = Stay_Data.objects.create(email=user, datein=datein, dateout=dateout, data=True, receiptJson=receipt, receiptid=receipt['consentReceiptID'])

    except Exception as e:
        return Response(f'Exception: {e}\n', status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_201_CREATED)


'''
    Remove user data of the influxdb by stay and the email
'''
@csrf_exempt
@api_view(('GET',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def removeDataUser(request):
    try:
        email = request.GET['userid']
        receiptid = request.GET['receipt_id']

        
        user = Contact.objects.get(email=email)
        qs = Stay_Data.objects.get(email=user, receiptid=receiptid)

        receipt = Receipt.objects.filter(stayId=qs)
        if not receipt.exists():
            

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

            now = timezone.now()
            Receipt.objects.create(email=user, timestamp=now, stayId=qs)
        
    except Exception as e:
        return Response(f'Exception: {e}\n', status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)



'''
    Validate data deletion
'''
@csrf_exempt
@api_view(('GET',))
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cleanData(request):
    try:
        email = request.GET['userid']
        receiptid = request.GET['receipt_id']
        
        user = Contact.objects.get(email=email)
        qs = Stay_Data.objects.get(email=user, receiptid=receiptid)

        receiptInfo = Receipt.objects.get(email=user, stayId=qs)
        
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

    