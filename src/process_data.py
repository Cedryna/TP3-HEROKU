import pandas as pd
from typing import List
import os
import glob
from pathlib import Path
import json
 
col_date: str = "date_heure"
col_donnees: str = "consommation"
cols: List[str] = [col_date, col_donnees]
fic_export_data: str = "data/interim/data.csv"
 
 
def load_data():
    list_fic: list[str] = [Path(e) for e in glob.glob("data/raw/*json")]
    list_df: list[pd.DataFrame] = []
    for p in list_fic:
        # list_df.append(pd.read_json(p))
        with open(p, "r") as f:
            dict_data: dict = json.load(f)
            df: pd.DataFrame = pd.DataFrame.from_dict(dict_data.get("results"))
            list_df.append(df)
 
    df: pd.DataFrame = pd.concat(list_df, ignore_index=True)
    return df
 
 
def format_data(df: pd.DataFrame):
    # typage
    df[col_date] = pd.to_datetime(df[col_date])
    # ordre
    df = df.sort_values(col_date)
    # filtrage colonnes
    df = df[cols]
    # dédoublonnage
    df = df.drop_duplicates()
    return df
 
 
def calculate_daily_average(df: pd.DataFrame):
    df["day_of_week"] = df[col_date].dt.day_name()
    daily_avg = df.groupby("day_of_week")[col_donnees].mean().reset_index()
    return daily_avg
 
 
def export_data(df: pd.DataFrame, filename: str):
    os.makedirs("data/interim/", exist_ok=True)
    df.to_csv(filename, index=False)
 
 
def main_process():
    df: pd.DataFrame = load_data()
    df = format_data(df)
    daily_avg = calculate_daily_average(df)
    export_data(df, fic_export_data)
    return daily_avg
 
 
if __name__ == "__main__":
    main_process()