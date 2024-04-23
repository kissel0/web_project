import requests


def get_culture_info(lat, lon):
    culture_info = []
    url = f"https://api.geoapify.com/v2/places?categories=entertainment.culture&filter=circle:{lon},{lat},500000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response = requests.get(url).json()
    for i in response['features']:
        try:
            x = i['properties']['name']
            culture_info.append(x)
        except:
            pass
    return culture_info


def get_nuturel_info(lat, lon):
    f = []
    cat = [('entertainment.zoo', 3), ('entertainment.planetarium', 3), ('natural', 10)]
    for i in cat:
        url = f"https://api.geoapify.com/v2/places?categories={i[0]}&filter=circle:{lon},{lat},500000&bias=proximity:{lon},{lat}&limit={i[-1]}&apiKey=23b70e7a81254e459c88d574598a37ab"
        response = requests.get(url)
        info = response.json()
        for j in info['features']:
            try:
                x = j['properties']['name']
                f.append(x)
            except:
                pass
    return f


def get_food_info(lat, lon):
    food_info = []
    url = f"https://api.geoapify.com/v2/places?categories=catering.restaurant&filter=circle:{lon},{lat},500000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response = requests.get(url)
    for i in response.json()['features']:
        try:
            x = i['properties']['name']
            food_info.append(x)
        except:
            pass
    url_2 = f"https://api.geoapify.com/v2/places?categories=catering.fast_food&filter=circle:{lon},{lat},500000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response_2 = requests.get(url_2)
    for j in response_2.json()['features']:
        try:
            x = j['properties']['name']
            food_info.append(x)
        except:
            pass
    url_3 = f"https://api.geoapify.com/v2/places?categories=catering.cafe&filter=circle:{lon},{lat},500000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response_3 = requests.get(url_3)
    for l in response_3.json()['features']:
        try:
            x = l['properties']['name']
            food_info.append(x)
        except:
            pass
    return food_info


def get_entertainment_info(lat, lon):
    entertainment_info = []
    url = f"https://api.geoapify.com/v2/places?categories=entertainment.cinema&filter=circle:{lon},{lat},500000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response = requests.get(url)
    for j in response.json()['features']:
        try:
            x = j['properties']['name']
            entertainment_info.append(x)
        except:
            pass
    url_2 = f"https://api.geoapify.com/v2/places?categories=entertainment.water_park&filter=circle:{lon},{lat},500000&bias=proximity:{lon},{lat}&limit=20&apiKey=23b70e7a81254e459c88d574598a37ab"
    response_2 = requests.get(url_2)
    for i in response_2.json()['features']:
        try:
            x = i['properties']['name']
            entertainment_info.append(x)
        except:
            pass
    return entertainment_info


print(get_entertainment_info(59.85367598, 30.152849675))
print(get_culture_info(59.85367598, 30.152849675))
print(get_food_info(59.85367598585305, 30.1528496750455))
print(get_nuturel_info(59.85367598585305, 30.1528496750455))
