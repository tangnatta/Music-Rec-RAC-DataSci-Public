import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


def load_music_db():
    file_path = os.path.join(current_dir, 'DB_music_full.parquet')
    return pd.read_parquet(file_path)
