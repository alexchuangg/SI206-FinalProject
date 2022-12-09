    for country in data:
        countries.append(country[1]['name'])
        population.append(country[1]['population'])
        female_life_expectancy.append(country[1]["life_expectancy_female"])
        male_life_expectancy.append(country[0]["life_expectancy_male"])
        internet_users.append(countries[1]['internet_users'])