from geopy.distance import geodesic

def calculate_distance(loc1, loc2):
    """Calculate distance in kilometers between two coordinates."""
    return geodesic(loc1, loc2).km
