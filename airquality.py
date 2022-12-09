import unittest
import sqlite3
import json
import os
import requests

API_Key = '6aa30181-6bb9-4f96-a17a-c6839fe06967'

def get_data(city):
    url = f'https://api.api-ninjas.com/v1/airquality?city={city}'
    try: 
        resp = requests.get(url, headers={'X-Api-Key': '6aa30181-6bb9-4f96-a17a-c6839fe06967'})
        data = json.loads(resp.text)
        print(data)
        return data

    except: 
        print('Exception')
        return None

get_data("Ann Arbor")