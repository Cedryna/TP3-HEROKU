import pandas as pd
from typing import List
import os
# Assume data is a list of dictionaries
def process_data(data: str):
    df = pd.read_csv(data, sep=";", parse_dates=["Date - Heure"])
    # Example processing: check for missing data
    # df = df.dropna()
    # sort_values per date
    df = df.sort_values("Date - Heure")
    return df

def filtre_data(df: pd.DataFrame, cols: List[str]):
    return df[cols]

def export_data(df: pd.DataFrame):
    os.makedirs("data/interim/", exist_ok=True)
    df.to_csv("data/interim/data.csv", index=False)

if __name__ == "__main__":

    data_file: str = "data/raw/eco2mix-regional-tr.csv"
    cols: List[str] = ["Date - Heure", "Consommation (MW)"]
    df: pd.DataFrame = process_data(data_file)
    df = filtre_data(df, cols)
    export_data(df)