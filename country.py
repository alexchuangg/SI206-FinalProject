import unittest
import sqlite3
import json
import os
import requests

API_Key = '6aa30181-6bb9-4f96-a17a-c6839fe06967'

def get_data(country):
    url = f'https://api.api-ninjas.com/v1/country?name={country}'

    try: 
        resp = requests.get(url, headers={'X-Api-Key': 'op+jNXkyR4hqbDr/7s+5yg==d1NJZb0OzNsLkset'})
        print(resp.text)

    except: 
        print('Exception')
        return None

get_data("United States")