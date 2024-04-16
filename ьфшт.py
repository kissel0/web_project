# sk-Rraq0mecQNN0sqYs1MIU9wtG1ML8NEk7
from pycountry_convert import country_alpha2_to_country_name, country_name_to_country_alpha2

city_name = input("Введите название города: ")

def get_airport_code(city_name):
    country_code = None
    for code in country_name_to_country_alpha2(city_name):
        country_code = code
        break

    if country_code:
        airport_code = country_alpha2_to_country_name(country_code)
        return airport_code
    else:
        return None

airport_code = get_airport_code(city_name)

if airport_code:
    print(f"Код аэропорта для города {city_name}: {airport_code}")
else:
    print(f"Аэропорт в городе {city_name} не найден.")