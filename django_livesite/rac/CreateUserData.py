import librosa
import numpy as np
from scipy.fft import fft, fftfreq, rfft, rfftfreq
import pandas as pd
import matplotlib.pyplot as plt
import math
import crepe
import os


def scoring(freq, note):
    note_freq = librosa.note_to_hz(note)
    if freq >= note_freq:
        return 1-(12*(math.log2(freq/note_freq)))
    else:
        return 1-(12*(math.log2(note_freq/freq)))


def user_data(file):
    user_pure_db = pd.DataFrame(
        columns=['user', 'song', 'time', 'frequency', 'confidence', 'note'])
    dfs = [user_pure_db]
    # load audio file
    y, sr = librosa.load(file)
    time, frequency, confidence, activation = crepe.predict(
        y, sr, model_capacity='tiny', viterbi=True)

    df = pd.DataFrame(
        {'time': time, 'frequency': frequency, 'confidence': confidence})
    # df['note']=df['frequency'].apply(lambda x: librosa.hz_to_note (x))

    # df['user'] = "Earth"
    df['song'] = os.path.basename(file)
    dfs.append(df.copy())
    # df.drop(columns=['file'], inplace=False).to_csv(os.path.join(SONG_PATH, dir, 'data.csv'), index=False) #! Obsolete Version
    # df.to_parquet(
    #     os.path.join("D:\\Github\\Music-Rec-RAC-DataSci\\Tee cover", 'รักแรกพบ.parquet'), index=False)

    music_pure_db = pd.concat(dfs, ignore_index=True)

    # music_pure_db.sort_values(by=['user', 'time'], inplace=True)
    music_pure_db['note'] = librosa.hz_to_note(music_pure_db['frequency'])

    # music_pure_db = music_pure_db[music_pure_db['confidence'] > 0.8] # thresholding to eliminate low confidence (noise)
    music_pure_db['score'] = music_pure_db.apply(
        lambda x: scoring(x['frequency'], x['note']), axis=1)

    # music_pure_db['score'].value_counts().sort_index()

    # music_pure_db.to_csv(os.path.join(
    #     "D:\\Github\\Music-Rec-RAC-DataSci\\Earth cover", 'รักแรกพบ - score.csv'), index=False)

    DB_music = pd.DataFrame(columns=['Name', 'E2_binary', 'F2_binary', 'F♯2_binary',
                                     'G2_binary', 'G♯2_binary', 'A2_binary', 'A♯2_binary', 'B2_binary',
                                     'C3_binary', 'C♯3_binary', 'D3_binary', 'D♯3_binary', 'E3_binary',
                                     'F3_binary', 'F♯3_binary', 'G3_binary', 'G♯3_binary', 'A3_binary',
                                     'A♯3_binary', 'B3_binary', 'C4_binary', 'C♯4_binary', 'D4_binary',
                                     'D♯4_binary', 'E4_binary', 'F4_binary', 'F♯4_binary', 'G4_binary',
                                     'G♯4_binary', 'A4_binary', 'A♯4_binary', 'B4_binary', 'C5_binary',
                                     'C♯5_binary', 'D5_binary', 'D♯5_binary', 'E5_binary', 'F5_binary',
                                     'F♯5_binary', 'G5_binary', 'G♯5_binary', 'A5_binary', 'A♯5_binary',
                                     'B5_binary', 'C6_binary', 'E2_score', 'F2_score', 'F♯2_score', 'G2_score',
                                     'G♯2_score', 'A2_score', 'A♯2_score', 'B2_score', 'C3_score', 'C♯3_score',
                                     'D3_score', 'D♯3_score', 'E3_score', 'F3_score', 'F♯3_score', 'G3_score',
                                     'G♯3_score', 'A3_score', 'A♯3_score', 'B3_score', 'C4_score', 'C♯4_score',
                                     'D4_score', 'D♯4_score', 'E4_score', 'F4_score', 'F♯4_score', 'G4_score',
                                     'G♯4_score', 'A4_score', 'A♯4_score', 'B4_score', 'C5_score', 'C♯5_score',
                                     'D5_score', 'D♯5_score', 'E5_score', 'F5_score', 'F♯5_score', 'G5_score',
                                     'G♯5_score', 'A5_score', 'A♯5_score', 'B5_score', 'C6_score'])

    for song in music_pure_db['song'].unique():
        # music_pure_db[music_pure_db['file']==song].to_csv(song+'.csv', index=False)
        cache = music_pure_db[music_pure_db['song'] == song]
        user = cache['user'].unique()[0]
        df = pd.DataFrame(cache['note'].value_counts().sort_index(
            key=lambda x: librosa.note_to_hz(x)))

        binary = df.copy()
        binary.index = binary.index + "_binary"
        binary['count'] = binary['count'].apply(
            lambda x: 1 if x > binary['count'].sum()*0.02 else 0)
        # binary.columns = ['count']

        df = pd.DataFrame(cache[['note', 'score']]).set_index('note')
        score = df.groupby(df.index).mean()
        score.index = score.index + "_score"
        score.columns = ['count']

        df = pd.concat([binary, score])
        df = df.transpose()

        df['Name'] = str(song) + " | " + str(user)

        DB_music = pd.concat([DB_music, df], ignore_index=True)

    DB_music[['E2_score', 'F2_score', 'F♯2_score', 'G2_score',
              'G♯2_score', 'A2_score', 'A♯2_score', 'B2_score', 'C3_score', 'C♯3_score',
              'D3_score', 'D♯3_score', 'E3_score', 'F3_score', 'F♯3_score', 'G3_score',
              'G♯3_score', 'A3_score', 'A♯3_score', 'B3_score', 'C4_score', 'C♯4_score',
              'D4_score', 'D♯4_score', 'E4_score', 'F4_score', 'F♯4_score', 'G4_score',
              'G♯4_score', 'A4_score', 'A♯4_score', 'B4_score', 'C5_score', 'C♯5_score',
              'D5_score', 'D♯5_score', 'E5_score', 'F5_score', 'F♯5_score', 'G5_score',
              'G♯5_score', 'A5_score', 'A♯5_score', 'B5_score', 'C6_score']] = DB_music[['E2_score', 'F2_score', 'F♯2_score', 'G2_score',
                                                                                         'G♯2_score', 'A2_score', 'A♯2_score', 'B2_score', 'C3_score', 'C♯3_score',
                                                                                         'D3_score', 'D♯3_score', 'E3_score', 'F3_score', 'F♯3_score', 'G3_score',
                                                                                         'G♯3_score', 'A3_score', 'A♯3_score', 'B3_score', 'C4_score', 'C♯4_score',
                                                                                         'D4_score', 'D♯4_score', 'E4_score', 'F4_score', 'F♯4_score', 'G4_score',
                                                                                         'G♯4_score', 'A4_score', 'A♯4_score', 'B4_score', 'C5_score', 'C♯5_score',
                                                                                         'D5_score', 'D♯5_score', 'E5_score', 'F5_score', 'F♯5_score', 'G5_score',
                                                                                         'G♯5_score', 'A5_score', 'A♯5_score', 'B5_score', 'C6_score']].fillna(0.63)

    return [0.65, 0.65, 0.65, 0.65]+[round(i[0], 2) for i in ((DB_music[['E2_score', 'F2_score', 'F♯2_score', 'G2_score',
                                                                        'G♯2_score', 'A2_score', 'A♯2_score', 'B2_score', 'C3_score', 'C♯3_score',
                                                                         'D3_score', 'D♯3_score', 'E3_score', 'F3_score', 'F♯3_score', 'G3_score',
                                                                         'G♯3_score', 'A3_score', 'A♯3_score', 'B3_score', 'C4_score', 'C♯4_score',
                                                                         'D4_score', 'D♯4_score', 'E4_score', 'F4_score', 'F♯4_score', 'G4_score',
                                                                         'G♯4_score', 'A4_score', 'A♯4_score', 'B4_score', 'C5_score', 'C♯5_score',
                                                                         'D5_score', 'D♯5_score', 'E5_score', 'F5_score', 'F♯5_score', 'G5_score',
                                                                         'G♯5_score', 'A5_score', 'A♯5_score', 'B5_score', 'C6_score']].to_dict().values()))] + [0.65, 0.65, 0.65, 0.65, 0.65]


if __name__ == "__main__":
    lst = user_data(
        "D:\\Github\\Music-Rec-RAC-DataSci\\django_livesite\\media\\user_voice\\รกแรกพบ_70NHdrV.mp3")
    print(lst)
    print(len(lst))
    print(type(lst))
