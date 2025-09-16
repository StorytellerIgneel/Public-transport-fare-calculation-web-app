from dataclasses import dataclass

@dataclass
class Station:
    name: str
    latitude: float
    longitude: float

@dataclass
class Fare:
    origin: Station
    destination: Station
    price: float

@dataclass
class Train:
    train_id: str
    line: str
    current_station: int #station id
    dir: int #1 for forward to id+1 station, -1 for backward to id-1 station
    progress: float #0.0-1.0 the progress between current_station and next station
    # speed: float #km/h
    timestamp: float #epoch time