import math
import random
from typing import List

from .models import Coordinate, SurroundingPoint

# Earth's mean radius in kilometers (WGS-84 sphere approximation)
EARTH_RADIUS_KM = 6371.01

def calculate_destination(start_coord: Coordinate, bearing_deg: float, distance_km: float) -> Coordinate:
    """
    Calculate the destination coordinate given a starting coordinate, bearing, and distance.
    Uses the Great Circle (spherical Earth) formula.
    
    :param start_coord: The starting Coordinate (lat, lon)
    :param bearing_deg: Bearing in degrees clockwise from North (0 to 360)
    :param distance_km: Distance to travel in kilometers
    :return: The destination Coordinate
    """
    # Convert latitude, longitude, and bearing to radians
    lat1 = math.radians(start_coord.latitude)
    lon1 = math.radians(start_coord.longitude)
    bearing = math.radians(bearing_deg)
    
    # Angular distance
    angular_dist = distance_km / EARTH_RADIUS_KM
    
    # Calculate destination latitude
    lat2 = math.asin(
        math.sin(lat1) * math.cos(angular_dist) +
        math.cos(lat1) * math.sin(angular_dist) * math.cos(bearing)
    )
    
    # Calculate destination longitude
    lon2 = lon1 + math.atan2(
        math.sin(bearing) * math.sin(angular_dist) * math.cos(lat1),
        math.cos(angular_dist) - math.sin(lat1) * math.sin(lat2)
    )
    
    # Normalize longitude to -180 to +180 degrees
    lon2 = (lon2 + math.pi) % (2 * math.pi) - math.pi
    
    # Convert back to degrees
    dest_lat = math.degrees(lat2)
    dest_lon = math.degrees(lon2)
    
    return Coordinate(latitude=dest_lat, longitude=dest_lon)


def generate_randomized_surrounding_points(
    center_coord: Coordinate,
    bearing_step: int = 10,
    min_dist_km: float = 5.0,
    max_dist_km: float = 15.0
) -> List[SurroundingPoint]:
    """
    Generate coordinates at every `bearing_step` (e.g., 10 degrees) from 0 to 360,
    each with a randomized distance between `min_dist_km` and `max_dist_km`.
    
    :param center_coord: The center coordinate of the target ship
    :param bearing_step: The bearing interval in degrees (default: 10)
    :param min_dist_km: Minimum distance in kilometers (default: 5.0)
    :param max_dist_km: Maximum distance in kilometers (default: 15.0)
    :return: A list of SurroundingPoint objects
    """
    points = []
    
    # Generate bearing angles (0, bearing_step, 2*bearing_step, ..., 360 - bearing_step)
    for bearing in range(0, 360, bearing_step):
        # Choose a random distance in the range [min_dist_km, max_dist_km]
        distance = random.uniform(min_dist_km, max_dist_km)
        
        # Calculate destination coordinate
        dest_coord = calculate_destination(center_coord, bearing, distance)
        
        points.append(
            SurroundingPoint(
                bearing=float(bearing),
                distance_km=distance,
                coordinate=dest_coord
            )
        )
        
    return points
