import pandas as pd
import math

NOTE = ['E2', 'F2', 'Gb2', 'G2', 'Ab2', 'A2', 'Bb2', 'B2', 'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3', 'A3', 'Bb3', 'B3', 'C4', 'Db4',
        'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5', 'C6']


def knn(df, user_val):
    df_song = df[['E2_binary', 'F2_binary', 'F♯2_binary', 'G2_binary', 'G♯2_binary',
                 'A2_binary', 'A♯2_binary', 'B2_binary', 'C3_binary', 'C♯3_binary',
                  'D3_binary', 'D♯3_binary', 'E3_binary', 'F3_binary', 'F♯3_binary',
                  'G3_binary', 'G♯3_binary', 'A3_binary', 'A♯3_binary', 'B3_binary',
                  'C4_binary', 'C♯4_binary', 'D4_binary', 'D♯4_binary', 'E4_binary',
                  'F4_binary', 'F♯4_binary', 'G4_binary', 'G♯4_binary', 'A4_binary',
                  'A♯4_binary', 'B4_binary', 'C5_binary', 'C♯5_binary', 'D5_binary',
                  'D♯5_binary', 'E5_binary', 'F5_binary', 'F♯5_binary', 'G5_binary',
                  'G♯5_binary', 'A5_binary', 'A♯5_binary', 'B5_binary', 'C6_binary',
                  'Name']].copy()
    df_freq = df[['E2_freq', 'F2_freq', 'F♯2_freq', 'G2_freq', 'G♯2_freq',
                 'A2_freq', 'A♯2_freq', 'B2_freq', 'C3_freq', 'C♯3_freq',
                  'D3_freq', 'D♯3_freq', 'E3_freq', 'F3_freq', 'F♯3_freq',
                  'G3_freq', 'G♯3_freq', 'A3_freq', 'A♯3_freq', 'B3_freq',
                  'C4_freq', 'C♯4_freq', 'D4_freq', 'D♯4_freq', 'E4_freq',
                  'F4_freq', 'F♯4_freq', 'G4_freq', 'G♯4_freq', 'A4_freq',
                  'A♯4_freq', 'B4_freq', 'C5_freq', 'C♯5_freq', 'D5_freq',
                  'D♯5_freq', 'E5_freq', 'F5_freq', 'F♯5_freq', 'G5_freq',
                  'G♯5_freq', 'A5_freq', 'A♯5_freq', 'B5_freq', 'C6_freq',]].copy()

    df_song['distance'] = None

    for i in range(len(df_song.index)):
        sumdis = 0
        for j in range(len(df_song.columns)-2):
            if df_song.iloc[i, j] == 0:
                continue
            # ignore if person can sing pitch but song doesn't have
            else:
                # print(df_song.iloc[i, j])
                sumdis += (user_val[j]-df_song.iloc[i, j])**2

        df_song.iat[i, list(df_song.columns).index(
            'distance')] = math.sqrt(sumdis)

    df_song['Occurance'] = None

    for i in range(len(df_song.index)):
        df_song.iat[i, list(df_song.columns).index(
            'Occurance')] = (
            float(sum(df_freq.iloc[i].astype(int).tolist())))

    df_song['score_fq'] = None

    for i in range(len(df_song.index)):
        sumfq = 0
        for j in range(len(NOTE)):
            sumfq += user_val[j]*df_freq.iloc[i][j]

        df_song.iat[i, list(df_song.columns).index(
            'score_fq')] = sumfq/df_song.iloc[i, list(df_song.columns).index(
                'Occurance')]*100

    df_song = df_song.sort_values(
        by=['score_fq', 'distance'], ascending=[False, True])

    return df_song


def avg(lst):
    if len(lst) <= 0:
        return 0
    return sum(lst)/len(lst)


table_head = ["#", "C2", "C♯2", "D2", "D♯2", "E2", "F2", "F♯2", "G2", "G♯2", "A2", "A♯2", "B2", "C3", "C♯3", "D3", "D♯3", "E3", "F3", "F♯3", "G3", "G♯3", "A3", "A♯3", "B3", "C4", "C♯4",
              "D4", "D♯4", "E4", "F4", "F♯4", "G4", "G♯4", "A4", "A♯4", "B4", "C5", "C♯5", "D5", "D♯5", "E5", "F5", "F♯5", "G5", "G♯5", "A5", "A♯5", "B5", "C6", "C#6", "D6", "D♯6", "E6", "F6"]


def performace_analysis(knn_res, user_val, current_song):
    df_res = knn_res.copy()
    df_res.set_index('Name', inplace=True)
    result_key = list(df_res['score_fq'].to_dict().keys())

    song = df_res[df_res.index == current_song].index[0]
    # result_key = list(df_res['score_fq'].to_dict().keys())
    # result_val = list(df_res['score_fq'].to_dict().values())

    # print(f"{df_res=}")

    song_note = {}

    song_note[song] = df_res.loc[song].transpose().map(
        lambda x: x if x == 1 else None).dropna().to_dict().keys()
    song_note[song] = [i.split("_")[0] for i in song_note[song]]

    # print(f"{song_note=}")

    user_song = {}

    val = song_note[song]

    lst_cahce = []
    for i in val:
        lst_cahce.append(user_val[table_head.index(i)-1])
    user_song[song] = lst_cahce

    # print(f"{user_song=}")

    max_user = max(user_song[song])*100
    min_user = min(user_song[song])*100

    def avg(lst):
        if len(lst) <= 0:
            return 0
        return sum(lst)/len(lst)

    val = user_song[song]

    avg_great_note = (avg([i for i in val if i > 0.85]))*100
    avg_medium_note = (avg([i for i in val if 0.7 < i <= 0.85]))*100
    avg_bad_note = (avg([i for i in val if 0.5 <= i <= 0.7]))*100

    avg_great_note = "N/A" if math.isnan(
        avg_great_note) or avg_great_note <= 0 else f"{avg_great_note:.2f}"
    avg_medium_note = "N/A" if math.isnan(
        avg_medium_note) or avg_medium_note <= 0 else f"{avg_medium_note:.2f}"
    avg_bad_note = "N/A" if math.isnan(
        avg_bad_note) or avg_bad_note <= 0 else f"{avg_bad_note:.2f}"

    len_great_note = (len([i for i in val if i > 0.85]))
    len_medium_note = (len([i for i in val if 0.7 < i <= 0.85]))
    len_bad_note = (len([i for i in val if 0.5 <= i <= 0.7]))

    overall_score = float(
        df_res[df_res.index == current_song]['score_fq'].iloc[0])

    return overall_score, max_user, avg_great_note, avg_medium_note, avg_bad_note, min_user
