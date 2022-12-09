import unittest
import sqlite3
import json
import os
import requests

API_Key = '6aa30181-6bb9-4f96-a17a-c6839fe06967'

def get_data(city):
    url = f'https://api.api-ninjas.com/v1/airquality?city={}'.format(city)

    response = requests.get(api_url, headers={'X-Api-Key': 'YOUR_API_KEY'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)

get_data("Ann Arbor")