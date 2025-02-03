import os
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

csv_file = os.path.join(parent_dir, 'Data Prep', 'DB_music_full.csv')

print(f"{csv_file=}")

DB_music = pd.read_csv(csv_file)
DB_music = DB_music.fillna(0)
DB_music.to_parquet(os.path.join(
    current_dir, 'DB_music_full.parquet'), index=True)

print(pd.read_parquet(os.path.join(current_dir, 'DB_music_full.parquet')))