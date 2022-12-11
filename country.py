import unittest
import sqlite3
import json
import os
import requests

def get_data(country):

    url = f'https://api.api-ninjas.com/v1/country?name={country}'

    try: 
        resp = requests.get(url, headers={'X-Api-Key': 'op+jNXkyR4hqbDr/7s+5yg==d1NJZb0OzNsLkset'})
        data = json.loads(resp.text)
        # print(data)
        return data

    except: 
        print('Exception')
        return None


# create personal table
def create_population_table(countries, cur, conn):

    cur.execute("CREATE TABLE IF NOT EXISTS country_data (country_id INTEGER PRIMARY KEY, country TEXT, population INTEGER, male_life_expectancy INTEGER, female_life_expectancy INTEGER, internet_users INTEGER)")

    cur.execute('SELECT country_id FROM country_data WHERE country_id  = (SELECT MAX(country_id) FROM country_data)')
    
    count = 0

    first = cur.fetchone()
    if (first == None):
        first = 0
    else:
        first = first[0] + 1

    for country in countries[first: first+25]:
        data = get_data(country)

        country_id = first + count
        countries_name = data[0]['name']
        population = data[0]['population']
        female_life_expectancy = data[0]["life_expectancy_female"]
        male_life_expectancy = data[0]["life_expectancy_male"]
        internet_users = data[0]['internet_users']

        cur.execute("INSERT OR IGNORE INTO country_data (country_id,country,population,male_life_expectancy,female_life_expectancy,internet_users) VALUES (?,?,?,?,?,?)",(country_id,countries_name,population,male_life_expectancy,female_life_expectancy,internet_users))

        count += 1

    conn.commit()

def create_gap_expectancies_table(cur, conn):

    country_ids = []
    gap_expectancies = []

    cur.execute("CREATE TABLE IF NOT EXISTS lifespan_gaps (country_id INTEGER PRIMARY KEY, gap_expectancies INTEGER)")

    cur.execute('SELECT country_id FROM country_data')
    ids = cur.fetchall()

    for id in ids:
        country_ids.append(id[0])

    cur.execute('SELECT (female_life_expectancy - male_life_expectancy) FROM country_data')
    gaps = cur.fetchall()

    for gap in gaps:
        gap_expectancies.append(gap[0])

    with open('gap_expectancies_calcs', 'w') as f:
        f.write("country_id, gap_expectancies")
        f.write('\n')
        for i in range(len(gap_expectancies)):
            f.write(str(country_ids[i]) + ", " + str(gap_expectancies[i]))
            f.write('\n')
    f.close()

    for i in range(len(ids)):
        cur.execute("INSERT OR IGNORE INTO lifespan_gaps (country_id,gap_expectancies) VALUES (?,?)",(country_ids[i],gap_expectancies[i]))
    conn.commit()



def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/country.db')
    cur = conn.cursor()

    countries = ['Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia', 'Botswana', 'Brazil', 'Bulgaria', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Costa Rica', "Cote d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kenya', "Korea", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Lithuania', 'Luxembourg', 'Macao', 'United States']
    # 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norfolk Island', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'United States', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, United States', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

    create_population_table(countries, cur, conn)
    create_gap_expectancies_table(cur, conn)
    print('added 25 rows of both tables to database')

if __name__ == "__main__":
    main()