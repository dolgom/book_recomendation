import urllib.parse
import requests
from geopy.distance import geodesic


def get_lat_lng(address, api_key):
    encoded = urllib.parse.quote_plus(address)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={encoded}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None


def calculate_closest_libraries(user_lat, user_lng, libraries, top_k=3):
    distances = []
    for lib in libraries:
        dist = geodesic((user_lat, user_lng), (lib["lat"], lib["lng"])).km
        distances.append({**lib, "distance": dist})
    return sorted(distances, key=lambda x: x["distance"])[:top_k]
