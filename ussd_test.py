import requests

url ="http://127.0.0.1:5000/ussd"

data ={
    "sessionId": "ATUssdSessionn1234",
    "serviceCode": "*123#",
    "phoneNumber": "254768798022",
    "text": ""
}

response = requests.post(url, data=data)
print(response.text)