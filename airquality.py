import unittest
import sqlite3
import json
import os
import requests

def get_data(country):

    url = f'https://api.api-ninjas.com/v1/airquality?city={country}'
    
    try: 
        resp = requests.get(url, headers={'X-Api-Key': 'op+jNXkyR4hqbDr/7s+5yg==d1NJZb0OzNsLkset'})
        data = json.loads(resp.text)
        # print(data)
        return data

    except: 
        print('Exception')
        return None

# create personal table
def create_air_quality_table(countries, cur, conn):

    cur.execute("CREATE TABLE IF NOT EXISTS air_quality (country_id INTEGER PRIMARY KEY, country TEXT, air_quality_index INTEGER, ozone_concentration INTEGER)")

    cur.execute('SELECT country_id FROM air_quality WHERE country_id  = (SELECT MAX(country_id) FROM air_quality)')
    
    count = 0

    first = cur.fetchone()
    if (first == None):
        first = 0
    else:
        first = first[0] + 1

    for country in countries[first: first+25]:
        data = get_data(country)

        country_id = first + count
        countries_name = country

        try:
            aqi = data['overall_aqi']
        except:
            aqi = -1

        try:
            ozone = data['O3']['concentration'] 
        except:
            ozone = -1

        cur.execute("INSERT OR IGNORE INTO air_quality (country_id,country,air_quality_index,ozone_concentration) VALUES (?,?,?,?)",(country_id,countries_name,aqi,ozone))

        count += 1

    conn.commit()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/country.db')
    cur = conn.cursor()

    countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia', 'Botswana', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kenya', "Korea", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macao', 'United States']

    create_air_quality_table(countries, cur, conn)
    print('added 25 rows to database')

if __name__ == "__main__":
    main()