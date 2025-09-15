import pandas as pd
import os

def convert_fare_table():
    #read csv
    df = pd.read_csv("src/components/backend/db_scripts/Fare.csv", index_col = 0)

    #melt into csv
    df_melted = df.reset_index().melt(id_vars="index", var_name="destination_id", value_name="fare")
    df_melted.rename(columns={"index": "origin_id"}, inplace=True)

    #get all unique station name
    all_stations = pd.unique(df_melted[['origin_id', 'destination_id']].values.ravel('K'))

    #auto id
    station_to_id = {station: i+1 for i, station in enumerate(all_stations)}

    # Map names → IDs
    df_melted["origin_id"] = df_melted["origin_id"].map(station_to_id)
    df_melted["destination_id"] = df_melted["destination_id"].map(station_to_id)
    #save to csv
    df_melted.to_csv("Fare_melted.csv", index=False)

    # produce id: name station csv
    # station_to_id is name → ID
    # Flip it into ID → name by reversig the dict
    id_to_station = {v: k for k, v in station_to_id.items()}

    # Turn into a DataFrame for saving
    stations_df = pd.DataFrame(list(id_to_station.items()), columns=["id", "station"])

    # Sort by ID
    stations_df = stations_df.sort_values("id").reset_index(drop=True)

    stations_df.to_csv("Stations.csv", index=False)

def convert_time_table():
    #read csv
    df = pd.read_csv("src/components/backend/db_scripts/Time.csv", index_col = 0)

    #melt into csv
    df_melted = df.reset_index().melt(id_vars="index", var_name="destination_id", value_name="time")
    df_melted.rename(columns={"index": "origin_id"}, inplace=True)

    #get all unique station name
    all_stations = pd.unique(df_melted[['origin_id', 'destination_id']].values.ravel('K'))

    #auto id
    station_to_id = {station: i+1 for i, station in enumerate(all_stations)}

    # Map names → IDs
    df_melted["origin_id"] = df_melted["origin_id"].map(station_to_id)
    df_melted["destination_id"] = df_melted["destination_id"].map(station_to_id)

    #save to csv
    df_melted.to_csv("Time_melted.csv", index=False)

# convert_time_table()