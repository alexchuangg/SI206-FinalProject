import unittest
import sqlite3
import json
import os
import requests
import matplotlib
import matplotlib.pyplot as plt

# need to output the results of the calculations to their own text files!

# calculation 1: gender expectancy gap (already a calculation) vs internet users scatterplot
def gender_gap_vs_internet_users(cur):
    gender_expectancies = []
    internet_users = []

    cur.execute("SELECT lifespan_gaps.gap_expectancies, country_data.internet_users FROM lifespan_gaps JOIN country_data ON lifespan_gaps.country_id = country_data.country_id")
    data = cur.fetchall()

    for country in data:
        gender_expectancies.append(country[0])
        internet_users.append(country[1])

    plt.scatter(gender_expectancies, internet_users)
    plt.xlabel('Yearly Lifespan Differences between Women and Men')
    plt.ylabel('The Percentage of Internet Users in each Country')
    plt.title('Gender Lifespan Differenes vs Internet Usage')
    plt.show()

# calculation 2: covid percentage vs internet users percentage (scatterplot)
def covid_vs_internet_users(cur):
    covid_totals = []
    population = []
    covid_percents = []
    internet_users1 = []
    ids = []

    cur.execute("SELECT covid_data.total_covid_cases, country_data.population, country_data.internet_users, country_data.country_id FROM covid_data JOIN country_data ON covid_data.country_id = country_data.country_id")
    data = cur.fetchall()

    for country in data:
        covid_totals.append(country[0])
        population.append(country[1])
        internet_users1.append(country[2])
        ids.append(country[3])

    del internet_users1[98]
    del internet_users1[90]
    del internet_users1[81]
    del internet_users1[76]
    del internet_users1[70]
    del internet_users1[69]
    del internet_users1[67]
    del internet_users1[60]
    del internet_users1[56]
    del internet_users1[44]
    del internet_users1[42]
    del internet_users1[37]
    del internet_users1[36]
    del internet_users1[29]
    del internet_users1[21]
    del internet_users1[18]
    del internet_users1[6]

    for i in range(len(covid_totals)):
        if covid_totals[i] > 0:
            percentage = covid_totals[i] / (population[i]*10)
            covid_percents.append(percentage)

    with open('covid_percentages_calcs.txt', 'w') as c:
        c.write("country_id, covid_percents")
        c.write('\n')
        for i in range(len(covid_percents)):
            c.write(str(ids[i]) + ", " + str(covid_percents[i]))
            c.write('\n')
    c.close()

    plt.scatter(covid_percents, internet_users1)
    plt.xlabel('Percentage of Covid Cases by Population Size')
    plt.ylabel('The Percentage of Internet Users in each Country')
    plt.title('Covid Case Percentage vs Internet Usage')
    plt.show()

# calculation 3: group countries by AQI category and create a bar graph of average the population size
# AQI categories: 0-50 = good, 51-100 = moderate, 101-150 = Unhealthy for some, 151-200 = Unhealthy, 201-300 = Very Unhealthy

def population_per_aqi_category(cur):
    aq_good = []
    aq_moderate = []
    aq_unhealthy_sensitive = []
    aq_unhealthy = []
    # aq_very_unhealthy = []

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
        # elif country[0] >= 201 and country[0] <= 300:
        #     aq_very_unhealthy.append(country)


    good_total = 0
    for country in aq_good:
        good_total += (country[1]*1000)
    good_avg = round(good_total/len(aq_good))

    moderate_total = 0
    for country in aq_moderate:
        moderate_total += (country[1]*1000)
    moderate_avg = round(moderate_total/len(aq_moderate))

    unhealthy_sensitive_total = 0
    for country in aq_unhealthy_sensitive:
        unhealthy_sensitive_total += (country[1]*1000)
    unhealthy_sensitive_avg = round(unhealthy_sensitive_total/len(aq_unhealthy_sensitive))

    unhealthy_total = 0
    for country in aq_unhealthy:
        unhealthy_total += (country[1]*1000)
    unhealthy_avg = round(unhealthy_total/len(aq_unhealthy))

    # very_unhealthy_total = 0
    # for country in aq_very_unhealthy:
    #     very_unhealthy_total += (country[1]*1000)
    # very_unhealthy_avg = round(very_unhealthy_total/len(aq_very_unhealthy))

    with open('aqi_vs_population.txt', 'w') as a:
        a.write("The average population size for a country with good air quality is " + str(good_avg) + ".")
        a.write('\n')
        a.write("The average population size for a country with moderate air quality is " + str(moderate_avg) + ".")
        a.write('\n')
        a.write("The average population size for a country with unhealthy (to sensitive groups) air quality is " + str(unhealthy_sensitive_avg) + ".")
        a.write('\n')
        a.write("The average population size for a country with unhealthy (to all groups) air quality is " + str(unhealthy_avg) + ".")
        a.write('\n')
        # a.write("The average population size for a country with very unhealthy air quality is " + str(very_unhealthy_avg) + ".")
        # a.write('\n')
    a.close()

    x_axis = ["Good", "Moderate", "Unhealthy (sensitive)", "Unhealthy (all)"]
    y_axis = [good_avg, moderate_avg, unhealthy_sensitive_avg, unhealthy_avg]

    plt.bar(x_axis, y_axis, color = 'orange')
    plt.xlabel('Air Quality Index Category')
    plt.ylabel('Average Country Population Size (100 millions)')
    plt.title('Air Quality vs Average Country Population Size')
    plt.show()


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/country.db')
    cur = conn.cursor()

    gender_gap_vs_internet_users(cur)
    covid_vs_internet_users(cur)
    population_per_aqi_category(cur)

if __name__ == "__main__":
    main()