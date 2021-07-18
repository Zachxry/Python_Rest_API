# python3
import requests

BASE = "http://127.0.0.1:5000/"

#response = requests.get(BASE + "customers") # send a GET request to return all customer data
#response = requests.get(BASE + "customers/1") # send a GET request with customer id

response = requests.post(BASE + "customers", {
    "customerId": 0,
    "first name": "Zach",
    "last name": "Marmolejo",
    "email": "Zachary.marmolejo@protonmail.com",
    "address": "9311 Somewhere lane",
    "city": "San Antonio",
    "state": "Texas",
    "zip code": "22224",} )

print(response)
print(response.json())

 