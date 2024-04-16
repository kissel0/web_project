import requests
from translate import Translator


# Функция для получения информации о стране через API OpenTripMap
def get_country_info(country_name):
    url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={country_name}&apikey=5ae2e3f221c38a28845f05b680412c05b68a17d373dabe83dffb5b7a"
    response = requests.get(url)
    lat, lon = response.json()['lat'], response.json()['lon']
    print(lat, lon)
    url_2 = f"https://api.geoapify.com/v2/places?categories=entertainment&filter=circle:{int(lon)},{int(lat)},9000000000000000000000000000000000000000000000000000000000&lang=en&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response_2 = requests.get(url_2)
    country_info = response_2.json()
    return country_info


# Функция для получения цен на билеты через API Flight Data
def get_flight_prices(from_city, to_city):
    url = f"https://api.flightdata.com/prices?from={from_city}&to={to_city}&apikey=661407AB679CC2D71F02C9B5"
    response = requests.get(url)
    flight_prices = response.json()
    return flight_prices


country_info = get_country_info("Rim")
for i in country_info['features']:
    print(i['properties']['name'])
