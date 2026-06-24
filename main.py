import sys
import argparse
from pathlib import Path

# Add src/ directory to python path for importing ship_navigator directly
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from ship_navigator import Coordinate, generate_randomized_surrounding_points

def main():
    parser = argparse.ArgumentParser(
        description="Calculate surrounding coordinates at every 10 degrees with a randomized distance of 5-15 km from a target ship."
    )
    parser.add_argument(
        "--lat",
        type=float,
        default=22.0,
        help="Latitude of the target ship (default: 22.0)"
    )
    parser.add_argument(
        "--lon",
        type=float,
        default=120.0,
        help="Longitude of the target ship (default: 120.0)"
    )
    parser.add_argument(
        "--bearing-step",
        type=int,
        default=10,
        help="Bearing step in degrees (default: 10)"
    )
    parser.add_argument(
        "--min-dist",
        type=float,
        default=5.0,
        help="Minimum distance in kilometers (default: 5.0)"
    )
    parser.add_argument(
        "--max-dist",
        type=float,
        default=15.0,
        help="Maximum distance in kilometers (default: 15.0)"
    )
    parser.add_argument(
        "--format",
        choices=["csv", "json", "plain"],
        default="plain",
        help="Output format: plain, csv, or json (default: plain)"
    )

    args = parser.parse_args()

    try:
        center = Coordinate(latitude=args.lat, longitude=args.lon)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate the points
    points = generate_randomized_surrounding_points(
        center_coord=center,
        bearing_step=args.bearing_step,
        min_dist_km=args.min_dist,
        max_dist_km=args.max_dist
    )

    # Output according to format
    if args.format == "json":
        import json
        output_data = [
            {
                "bearing_deg": pt.bearing,
                "distance_km": round(pt.distance_km, 3),
                "latitude": round(pt.coordinate.latitude, 6),
                "longitude": round(pt.coordinate.longitude, 6)
            }
            for pt in points
        ]
        print(json.dumps(output_data, indent=2))
        
    elif args.format == "csv":
        print("bearing_deg,distance_km,latitude,longitude")
        for pt in points:
            print(f"{pt.bearing},{pt.distance_km:.3f},{pt.coordinate.latitude:.6f},{pt.coordinate.longitude:.6f}")
            
    else: # plain
        print(f"Target Ship Location: Lat {center.latitude:.6f}, Lon {center.longitude:.6f}")
        print(f"Surrounding Coordinates (every {args.bearing_step}° bearing, random {args.min_dist}-{args.max_dist} km):")
        print("-" * 70)
        print(f"{'Bearing (°)':<12} | {'Distance (km)':<15} | {'Latitude':<15} | {'Longitude':<15}")
        print("-" * 70)
        for pt in points:
            print(f"{pt.bearing:<12.1f} | {pt.distance_km:<15.3f} | {pt.coordinate.latitude:<15.6f} | {pt.coordinate.longitude:<15.6f}")
        print("-" * 70)
        print(f"Total generated points: {len(points)}")

if __name__ == "__main__":
    main()
