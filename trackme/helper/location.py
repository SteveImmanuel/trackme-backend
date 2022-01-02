import math

EARTH_RADIUS = 6378137 # in m

def calculate_distance(lat1, long1, lat2, long2):
    delta_lat = math.radians(lat2- lat1)
    delta_long = math.radians(long2-long1)

    a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(delta_long / 2) * math.sin(delta_long / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS * c