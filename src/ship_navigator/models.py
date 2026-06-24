from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    """Represents a geographic coordinate with latitude and longitude."""
    latitude: float
    longitude: float

    def __post_init__(self):
        # Validate latitude
        if not -90.0 <= self.latitude <= 90.0:
            raise ValueError(f"Latitude must be between -90 and 90 degrees. Got: {self.latitude}")
        # Validate longitude
        if not -180.0 <= self.longitude <= 180.0:
            raise ValueError(f"Longitude must be between -180 and 180 degrees. Got: {self.longitude}")


@dataclass(frozen=True)
class SurroundingPoint:
    """Represents a generated point relative to a target ship."""
    bearing: float       # in degrees (0 to 360)
    distance_km: float   # in kilometers
    coordinate: Coordinate
