import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep


stations = pd.read_csv("Stations.csv")

# Initialize geocoder
geolocator = Nominatim(user_agent="station_locator")

# Store results
latitudes = []
longitudes = []

for station in stations["station"]:
    try:

        if "(KJL)" in station:
            query = f"{station.replace('(KJL)', '').strip()} LRT"
        elif "(SBK)" in station:
            query = f"{station.replace('(SBK)', '').strip()} MRT"
        else:

            query = f"{station} Station"

        location = geolocator.geocode(query)

        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
            print(f"✅ Found: {station} -> ({location.latitude}, {location.longitude})")
        else:
            latitudes.append(None)
            longitudes.append(None)
            print(f"⚠️ Not found: {station}")

    except Exception as e:
        latitudes.append(None)
        longitudes.append(None)
        print(f"❌ Error fetching {station}: {e}")

    sleep(1)



stations["Latitude"] = latitudes
stations["Longitude"] = longitudes

# Save results
stations.to_csv("stations_with_coords_2.csv", index=False)
print("✅ Saved -> stations_with_coords_2.csv")
