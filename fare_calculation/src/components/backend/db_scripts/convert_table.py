import pandas as pd
import os

def convert_fare_table():
    #read csv
    df = pd.read_csv("src/components/backend/db_scripts/Fare.csv", index_col = 0)

    #melt into csv
    df_melted = df.reset_index().melt(id_vars="index", var_name="destination", value_name="fare")
    df_melted.rename(columns={"index": "origin_station"}, inplace=True)

    #save to csv
    df_melted.to_csv("Fare_melted.csv", index=False)

def convert_time_table():
    #read csv
    df = pd.read_csv("src/components/backend/db_scripts/Time.csv", index_col = 0)

    #melt into csv
    df_melted = df.reset_index().melt(id_vars="index", var_name="destination", value_name="time")
    df_melted.rename(columns={"index": "origin_station"}, inplace=True)

    #save to csv
    df_melted.to_csv("Time_melted.csv", index=False)

convert_time_table()