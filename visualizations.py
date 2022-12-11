import unittest
import sqlite3
import json
import os
import requests
import matplotlib
import matplotlib.pyplot as plt

# need to output the results of the calculations to their own text files!

# calculation 1: gender expectancy gap (already a calculation) vs covid cases scatterplot

# calculation 2: covid cases / total population by country

# calculation 3: group countries by AQI category and create a bar graph of average the population size
# AQI categories: 0-50 = good, 51-100 = moderate, 101-150 = Unhealthy for some, 151-200 = Unhealthy, 201-300 = Very Unhealthy

def population_per_aqi_category(cur):
    aq_good = []
    aq_moderate = []
    aq_unhealthy_sensitive = []
    aq_unhealthy = []
    aq_very_unhealthy = []

    cur.execute("SELECT air_quality.air_quality_index, country_data.population FROM air_quality JOIN country_data ON air_quality.country_id = country_data.country_id")
    data = cur.fetchall()

    for country in data:
        if country[0] >= 0 and country[0] <= 50:
            aq_good.append(country)
        elif country[0] >= 51 and country[0] <= 100:
            aq_moderate.append(country)
        elif country[0] >= 101 and country[0] <= 150:
            aq_unhealthy_sensitive.append(country)
        elif country[0] >= 151 and country[0] <= 200:
            aq_unhealthy.append(country)
        elif country[0] >= 201 and country[0] <= 300:
            aq_very_unhealthy.append(country)

    good_total = 0
    for country in aq_good:
        good_total += country[1]
    good_avg = round(good_total/len(aq_good))

    moderate_total = 0
    for country in aq_moderate:
        moderate_total += country[1]
    moderate_avg = round(moderate_total/len(aq_moderate))

    unhealthy_sensitive_total = 0
    for country in aq_unhealthy_sensitive:
        unhealthy_sensitive_total += country[1]
    unhealthy_sensitive_avg = round(unhealthy_sensitive_total/len(aq_unhealthy_sensitive))

    unhealthy_total = 0
    for country in aq_unhealthy:
        unhealthy_total += country[1]
    unhealthy_avg = round(unhealthy_total/len(aq_unhealthy))

    very_unhealthy_total = 0
    for country in aq_very_unhealthy:
        very_unhealthy_total += country[1]
    very_unhealthy_avg = round(very_unhealthy_total/len(aq_very_unhealthy))

    with open('aqi_vs_population.txt', 'w') as f:
        f.write("The average population size for a country with good air quality is " + str(good_avg) + ".")
        f.write('\n')
        f.write("The average population size for a country with moderate air quality is " + str(moderate_avg) + ".")
        f.write('\n')
        f.write("The average population size for a country with unhealthy (to sensitive groups) air quality is " + str(unhealthy_sensitive_avg) + ".")
        f.write('\n')
        f.write("The average population size for a country with unhealthy (to all groups) air quality is " + str(unhealthy_avg) + ".")
        f.write('\n')
        f.write("The average population size for a country with very unhealthy air quality is " + str(very_unhealthy_avg) + ".")
        f.write('\n')
    f.close()

    x_axis = ["Good", "Moderate", "Unhealthy (sensitive)", "Unhealthy (all)", "Very Unhealthy"]
    y_axis = [good_avg, moderate_avg, unhealthy_sensitive_avg, unhealthy_avg, very_unhealthy_avg]

    plt.bar(x_axis, y_axis, color = 'orange')
    plt.xlabel('Air Quality Index Category')
    plt.ylabel('Average Country Population Size')
    plt.title('Air Quality vs Average Country Population Size')
    plt.show()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/country.db')
    cur = conn.cursor()

    population_per_aqi_category(cur)

if __name__ == "__main__":
    main()