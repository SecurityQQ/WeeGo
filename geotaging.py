import requests as r
import json

token = "AIzaSyBjNOY8PKIC4n0YT8tukPE0HaSJ_HKGmD8"

def get_places_nearby(lat=None, lng=None, radius=500, type=None, name=None):
    """

    :param lat:
    :param lng:
    :param radius: in meters
    :param type: type of place
    :param name: name of place (or substr)
    :return: [{'lat': 41.39057340000001, 'lng': 2.1155788, 'name': 'Piña Colada', 'vicinity': "Plaça d'Eusebi Güell, 13, Barcelona"}]
    """

    if lat is None:
        lat = 41.388004
    if lng is None:
        lng = 2.113280

    name_part = ""
    if name is not None:
        name_part = "&name={}".format(name)

    type_part = ""
    if type is not None:
        type_part = "&type={}".format(type)

    key_part = "&key={}".format(token)

    base = "https://maps.googleapis.com/maps/api/place/nearbysearch"
    location = "/json?location={},{}&radius={}".format(lat, lng, radius)

    url = base + location + type_part + name_part + key_part

    content = json.loads(r.get(url).content)

    results = []
    if content['status'] == 'ZERO_RESULTS':
        return results

    for i, result in enumerate(content["results"]):
        try:
            res = {}
            res['lat'] = content["results"][i]["geometry"]["location"]["lat"]
            res['lng'] = content["results"][i]["geometry"]["location"]["lng"]
            res['name'] = content["results"][i]["name"]
            res["vicinity"] = content["results"][i]["vicinity"]
            results.append(res)
        except Exception as e:
            print(e)
    return results

print(get_places_nearby(radius=1000, name="sinema"))