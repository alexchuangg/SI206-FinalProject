import unittest
import sqlite3
import json
import os
import requests

API_Key = '6aa30181-6bb9-4f96-a17a-c6839fe06967'

def get_data():
    url = f'https://api.api-ninjas.com/v1/country?name='

    try: 
        resp = requests.get(url, headers={'X-Api-Key': 'op+jNXkyR4hqbDr/7s+5yg==d1NJZb0OzNsLkset'})
        data = json.loads(resp.text)
        # print(data)
        return data

    except: 
        print('Exception')
        return None


# create personal table
def create_population_table(data, cur, conn):

    countries = []
    population = []
    male_life_expectancy = []
    female_life_expectancy = []
    internet_users = []
    
    for country in data:
        countries.append(country[1]['name'])
        population.append(country[1]['population'])
        female_life_expectancy.append(country[1]["life_expectancy_female"])
        male_life_expectancy.append(country[0]["life_expectancy_male"])
        internet_users.append(countries[1]['internet_users'])

    cur.execute("CREATE TABLE IF NOT EXISTS Population (country TEXT PRIMARY KEY, population INTEGER, male_life_expectancy INTEGER, internet_users INTEGER)")

    for i in range(len(countries)):
        cur.execute("INSERT INTO Population (country,population,male_life_expectancy, female_life_expectancy, internet_users) VALUES (?,?,?,?,?)",(countries[i],population[i],male_life_expectancy[i],internet_users[i]))
    conn.commit()

    # calculate the gap between female and male life expectancies
    gap_expectancies = []
    for i in range(len(countries)):
        gap_expectancies.append(male_life_expectancy[i] - female_life_expectancy[i])

    for i in range(len(countries)):
        cur.execute("UPDATE Population SET gap_expectancies = ? WHERE country = ?", (gap_expectancies[i], countries[i]))
    conn.commit()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/country.db')
    cur = conn.cursor()

    data = get_data()
    create_population_table(data, cur, conn)

if __name__ == "__main__":
    main()