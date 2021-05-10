#!/usr/bin/env bash

# Insert stay
echo -e "Insert stay"
#content=$(curl -s -d "{\"start_date\": \"2021-04-20\", \"end_date\": \"2021-04-22\", \"userid\": \"my@email.com\", \"receipt\": {\"subjectEmail\":\"user@email.com\"}}" \
#-H "Content-Type: application/json" http://atnog-homeassistant.av.it.pt:8000/stay/add)

content=$(curl -s -d "{\"start_date\": \"2021-04-20\", \"end_date\": \"2021-04-22\", \"userid\": \"my@email.com\", \"receipt\": {\"receipt_id\":\"2\"}}" \
-H "Content-Type: application/json" http://localhost:8000/stay/add)

stay_id=$( jq -r  '.stay_id' <<< "${content}" ) 
echo -e "stay_id= ${stay_id}"


# Remove personal data of the renter
echo -e "Remove personal data of the renter"
#curl -s -X GET "http://atnog-homeassistant.av.it.pt:8000/stay/delete?token='123ABC'&email: my@email.com&receiptid=2"

curl -s -X GET "http://localhost:8000/stay/delete?token='123ABC'&email: my@email.com&receiptid=2"


# Validate data deletion
echo -e "Validate data deletion"
#curl -s -X GET "http://atnog-homeassistant.av.it.pt:8000/stay/clean?token='123ABC'&email: my@email.com&receiptid=2"

curl -s -X GET "http://localhost:8000/stay/clean?token='123ABC'&email: my@email.com&receiptid=2"
