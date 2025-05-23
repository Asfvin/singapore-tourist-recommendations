import geocoder
import folium


SINGAPORE_ATTRACTIONS = {
    "Marina Bay Sands": {"lat": 1.282302, "lon": 103.858528},
    "Gardens by the Bay": {"lat": 1.282375, "lon": 103.864273},
    "Sentosa Island": {"lat": 1.250111, "lon": 103.830933},
    "Merlion Park": {"lat": 1.286788, "lon": 103.854531},
    "Singapore Flyer": {"lat": 1.289332, "lon": 103.863223},
    "Orchard Road": {"lat": 1.304833, "lon": 103.831833},
    "Singapore Zoo": {"lat": 1.404348, "lon": 103.793023},
    "Chinatown": {"lat": 1.2842, "lon": 103.8436},
    "Little India": {"lat": 1.3066, "lon": 103.8519},
    "Clarke Quay": {"lat": 1.2906, "lon": 103.8465},
}

icon_star = folium.Icon(
    prefix="fa",
    icon="star",
    icon_color="blue",
)

icon_attraction = folium.Icon(color="green", icon="info-sign")


def get_current_location():
    g = geocoder.ip("me")  # Fetch location using IP address
    latitude, longitude = g.latlng  # Extract latitude and longitude

    return latitude, longitude
