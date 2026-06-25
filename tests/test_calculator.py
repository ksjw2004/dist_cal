import unittest
import sys
from pathlib import Path

# Add src/ directory to python path for importing ship_navigator directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ship_navigator import Coordinate, calculate_destination, generate_randomized_surrounding_points, generate_random_targets

class TestShipNavigator(unittest.TestCase):
    
    def test_coordinate_validation(self):
        # Valid coordinates
        coord = Coordinate(25.0, 121.0)
        self.assertEqual(coord.latitude, 25.0)
        self.assertEqual(coord.longitude, 121.0)
        
        # Invalid latitude
        with self.assertRaises(ValueError):
            Coordinate(95.0, 120.0)
        with self.assertRaises(ValueError):
            Coordinate(-91.0, 120.0)
            
        # Invalid longitude
        with self.assertRaises(ValueError):
            Coordinate(25.0, 185.0)
        with self.assertRaises(ValueError):
            Coordinate(25.0, -181.0)

    def test_calculate_destination_north(self):
        # Start at equator, prime meridian
        start = Coordinate(0.0, 0.0)
        # 111.12 km is roughly 1 degree of latitude
        dest = calculate_destination(start, bearing_deg=0.0, distance_km=111.12)
        
        # We expect bearing 0 to lead straight North (longitude remains 0, latitude increases)
        self.assertAlmostEqual(dest.longitude, 0.0, places=5)
        self.assertGreater(dest.latitude, 0.0)
        # Expected latitude is roughly 1.0 degree
        self.assertAlmostEqual(dest.latitude, 1.0, places=1)

    def test_calculate_destination_east(self):
        # Start at equator, prime meridian
        start = Coordinate(0.0, 0.0)
        # 111.12 km is roughly 1 degree of longitude at the equator
        dest = calculate_destination(start, bearing_deg=90.0, distance_km=111.12)
        
        # We expect bearing 90 to lead straight East at the equator (latitude remains 0, longitude increases)
        self.assertAlmostEqual(dest.latitude, 0.0, places=5)
        self.assertGreater(dest.longitude, 0.0)
        # Expected longitude is roughly 1.0 degree
        self.assertAlmostEqual(dest.longitude, 1.0, places=1)

    def test_generate_randomized_surrounding_points(self):
        center = Coordinate(25.0330, 121.5654) # Taipei
        points = generate_randomized_surrounding_points(
            center_coord=center,
            bearing_step=10,
            min_dist_km=5.0,
            max_dist_km=15.0
        )
        
        # We expect 36 points (360 / 10)
        self.assertEqual(len(points), 36)
        
        # Check bearing and distance boundaries
        for idx, pt in enumerate(points):
            # Check expected bearings: 0, 10, 20, ..., 350
            expected_bearing = float(idx * 10)
            self.assertEqual(pt.bearing, expected_bearing)
            
            # Check randomized distance is within range [5.0, 15.0]
            self.assertTrue(5.0 <= pt.distance_km <= 15.0)
            
            # Check resulting coordinate is valid
            self.assertTrue(-90.0 <= pt.coordinate.latitude <= 90.0)
            self.assertTrue(-180.0 <= pt.coordinate.longitude <= 180.0)

    def test_generate_random_targets(self):
        lat_min, lat_max = 22.0, 25.0
        lon_min, lon_max = 119.0, 122.0
        num_targets = 100
        
        targets = generate_random_targets(
            num_targets=num_targets,
            lat_min=lat_min,
            lat_max=lat_max,
            lon_min=lon_min,
            lon_max=lon_max
        )
        
        self.assertEqual(len(targets), num_targets)
        for target in targets:
            self.assertTrue(lat_min <= target.latitude <= lat_max)
            self.assertTrue(lon_min <= target.longitude <= lon_max)

if __name__ == "__main__":
    unittest.main()

