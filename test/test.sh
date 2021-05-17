#!/usr/bin/env bash

# Insert stay
echo -e "Insert stay"
#curl -s -d "{\"start_date\": \"2021-04-20 00:00:00\", \"end_date\": \"2021-04-22 00:00:00\", \"userid\": \"my@email.com\", \"receipt\": {\"consentReceiptID\":\"c8c37806-ef54-4d1b-a741-39f6e1868019\"}}" \
#-H "Authorization: Token 05d179c1a1b84dbc907a2deb900931e8fb03140f" -H "Content-Type: application/json" http://atnog-homeassistant.av.it.pt:8000/stay/add

curl -s -d "{\"start_date\": \"2021-04-20 00:00:00\", \"end_date\": \"2021-04-22 00:00:00\", \"userid\": \"my@email.com\", \"receipt\": {\"consentReceiptID\":\"c8c37806-ef54-4d1b-a741-39f6e1868019\"}}" \
-H "Authorization: Token 74bd3673e5b76918c4fb6f0d9e8bbd9c25ff9b24" -H "Content-Type: application/json" http://localhost:8000/stay/add


# Remove personal data of the renter
#echo -e "Remove personal data of the renter"
#curl -s -H "Authorization: Token 05d179c1a1b84dbc907a2deb900931e8fb03140f" -X GET "http://atnog-homeassistant.av.it.pt:8000/stay/delete?token='123ABC'&userid=my@email.com&receipt_id=c8c37806-ef54-4d1b-a741-39f6e1868019"

curl -s -H "Authorization: Token 74bd3673e5b76918c4fb6f0d9e8bbd9c25ff9b24" -X GET "http://localhost:8000/stay/delete?userid=my@email.com&receipt_id=c8c37806-ef54-4d1b-a741-39f6e1868019"


# Validate data deletion
#echo -e "Validate data deletion"
#curl -s -H "Authorization: Token 05d179c1a1b84dbc907a2deb900931e8fb03140f" -X GET "hhttp://atnog-homeassistant.av.it.pt:8000/stay/clean?token='123ABC'&userid=my@email.com&receipt_id=c8c37806-ef54-4d1b-a741-39f6e1868019"

curl -s -H "Authorization: Token 74bd3673e5b76918c4fb6f0d9e8bbd9c25ff9b24" -X GET "http://localhost:8000/stay/clean?userid=my@email.com&receipt_id=c8c37806-ef54-4d1b-a741-39f6e1868019"
