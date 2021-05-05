#!/usr/bin/env bash

# Insert stay
echo -e "Remove data"
curl -s -d "{\"start_date\": \"2021-04-20\", \"end_date\": \"2021-04-22\", \"stay_id\":\"reservation_id\", \"receipts\": {}}" \
-H "Content-Type: application/json" http://atnog-homeassistant.av.it.pt:8000/stay/clean:8000/stay/delete


echo -e "Validate data deletion"
curl -s -d "{\"start_date\": \"2021-04-20\", \"end_date\": \"2021-04-22\", \"stay_id\":\"reservation_id\", \"receipts\": {}}" \
 -X GET "http://atnog-homeassistant.av.it.pt:8000/stay/clean:8000/stay/clean" | jq .
