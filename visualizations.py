import unittest
import sqlite3
import json
import os
import requests

# need to output the results of the calculations to their own text files!

# calculation 1: gender expectancy gap (already a calculation) vs covid cases scatterplot

# calculation 2: covid cases / total population by country

# calculation 3: group countries by AQI category and create a bar graph of average the population size
# AQI categories: 0-50 = good, 51-100 = moderate, 101-150 = Unhealthy, 201-300 = Very Unhealthy


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/country.db')
    cur = conn.cursor()

if __name__ == "__main__":
    main()