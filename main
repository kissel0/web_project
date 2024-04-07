import requests

# Функция для получения информации о стране через API OpenTripMap
def get_country_info(country_name):
    url = f"https://api.opentripmap.com/0.1/en/places/geoname?name={country_name}&apikey=5ae2e3f221c38a28845f05b680412c05b68a17d373dabe83dffb5b7a"
    response = requests.get(url)
    lat, lon = response.json()['lat'], response.json()['lon']
    url_2 = f"https://api.opentripmap.com/0.1/ru/places/radius?radius=500000000000&lon={int(lon)}&lat={int(lat)}&limit=10&apikey=5ae2e3f221c38a28845f05b680412c05b68a17d373dabe83dffb5b7a"
    response_2 = requests.get(url_2)
    country_info = response_2.json()
    return country_info

# Функция для получения цен на билеты через API Flight Data
def get_flight_prices(from_city, to_city):
    url = f"https://api.flightdata.com/prices?from={from_city}&to={to_city}&apikey=5ae2e3f221c38a28845f05b680412c05b68a17d373dabe83dffb5b7a"
    response = requests.get(url)
    flight_prices = response.json()
    return flight_prices

# Функция для обеспечения безопасного обмена данными через API ProxyAPI
# def proxy_request(url):
#     proxy_url = "https://api.proxyapi.io/request"
#     payload = {
#         "url": url,
#         "apikey": "YOUR_API_KEY"
#     }
#     response = requests.post(proxy_url, json=payload)
#     data = response.json()
#     return data

# Пример использования функций
country_info = get_country_info("France")
print(country_info)

# flight_prices = get_flight_prices("New York", "Paris")
# print(flight_prices)
#
# data = proxy_request("https://api.opentripmap.com/0.1/en/places/geoname?name=France&apikey=YOUR_API_KEY")
# print(data)
