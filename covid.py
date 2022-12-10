import unittest
import sqlite3
import json
import os
import requests

def get_data(country):
    url = f'https://api.api-ninjas.com/v1/covid19?country={country}'
    try: 
        resp = requests.get(url, headers={'X-Api-Key': 'op+jNXkyR4hqbDr/7s+5yg==d1NJZb0OzNsLkset'})
        data = json.loads(resp.text)
        # print(data)
        return data

    except: 
        print('Exception')
        return None

# create personal table
def create_covid_table(countries, cur, conn):

    cur.execute("CREATE TABLE IF NOT EXISTS covid_data (country_id INTEGER PRIMARY KEY, country TEXT, total_covid_cases INTEGER)")

    cur.execute('SELECT country_id FROM covid_data WHERE country_id  = (SELECT MAX(country_id) FROM covid_data)')
    
    count = 0

    first = cur.fetchone()
    if (first == None):
        first = 0
    else:
        first = first[0] + 1

    for country in countries[first: first+25]:
        covid_cases = 0

        data = get_data(country)

        country_id = first + count
        countries_name = country

        try:
            for i in range(len(data)):
                covid_cases += data[i]['cases']['2022-12-08']['total']
        except:
            covid_cases = -1
        
        if covid_cases == 0:
            covid_cases = -1


        cur.execute("INSERT OR IGNORE INTO covid_data (country_id,country,total_covid_cases) VALUES (?,?,?)",(country_id,countries_name,covid_cases))

        count += 1

    conn.commit()

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/country.db')
    cur = conn.cursor()

    countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia', 'Botswana', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kenya', "Korea", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macao', 'United States']

    create_covid_table(countries, cur, conn)
    print('added 25 rows to database')

if __name__ == "__main__":
    main()