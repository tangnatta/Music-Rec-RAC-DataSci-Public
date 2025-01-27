import pandas as pd
from django.shortcuts import render, HttpResponse
import math
from .forms import VoiceForm
from .models import Voice
from .CreateUserData import user_data
# Create your views here.
table_head = ["#", "C2", "C♯2", "D2", "D♯2", "E2", "F2", "F♯2", "G2", "G♯2", "A2", "A♯2", "B2", "C3", "C♯3", "D3", "D♯3", "E3", "F3", "F♯3", "G3", "G♯3", "A3", "A♯3", "B3", "C4", "C♯4",
              "D4", "D♯4", "E4", "F4", "F♯4", "G4", "G♯4", "A4", "A♯4", "B4", "C5", "C♯5", "D5", "D♯5", "E5", "F5", "F♯5", "G5", "G♯5", "A5", "A♯5", "B5", "C6", "C#6", "D6", "D♯6", "E6", "F6"]
user_val = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.87, 0.87, 0.89, 0.73, 0.99, 0.57, 0.89, 0.99, 0.74, 0.62, 0.91, 0.53, 0.91, 0.66, 1.0, 0.71, 0.65,
            0.95, 0.83, 0.85, 0.76, 0.77, 0.65, 0.92, 0.95, 0.82, 0.87, 0.86, 0.85, 0.52, 0.85, 0.95, 0.89, 0.69, 0.82, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
NOTE = ['E2', 'F2', 'Gb2', 'G2', 'Ab2', 'A2', 'Bb2', 'B2', 'C3', 'Db3', 'D3', 'Eb3', 'E3', 'F3', 'Gb3', 'G3', 'Ab3', 'A3', 'Bb3', 'B3', 'C4', 'Db4',
        'D4', 'Eb4', 'E4', 'F4', 'Gb4', 'G4', 'Ab4', 'A4', 'Bb4', 'B4', 'C5', 'Db5', 'D5', 'Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab5', 'A5', 'Bb5', 'B5', 'C6']
user_new = []

# Read Online Dataset
# df = pd.read_csv(
#     'https://tangnatta.github.io/Music-Rec-RAC-DataSci/DB_music_full.csv')
df = pd.read_csv('./rac/DB_music_full.csv')
df = df.fillna(0)

user_df = pd.DataFrame([['test']+user_val], columns=table_head)


def random_user_val():
    import random
    for i in range(len(user_val)):
        if user_val[i] > 0.85:
            user_val[i] = random.randint(86, 100)/100
        elif user_val[i] > 0.7:
            user_val[i] = random.randint(71, 85)/100
        elif user_val[i] >= 0.5:
            user_val[i] = random.randint(50, 70)/100
    return user_val


def knn(user_val):
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


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def error_404(request):
    return render(request, "404.html", {'home_link': '../home'})


def test(request):
    return render(request, "base.html", {'this_page': ''})


def home(request):
    # random_user_val()
    return render(request, "home.html", {'this_page': 'home', 'table_head': table_head, 'table_content': user_val})


def karaoke(request):
    global user_val
    form = VoiceForm(request.POST, request.FILES)
    if request.method == 'POST':
        voice = Voice(voice=request.FILES['voice'])
        voice.save()

        # print(Voice.objects.all().last().voice.path)
        user_val = user_data(Voice.objects.all().last().voice.path)
        return home(request)
    return render(request, "karaoke.html", {'this_page': 'karaoke', 'state': "", 'form': form})


def karaoke_started(request):
    global user_val
    form = VoiceForm(request.POST, request.FILES)
    if request.method == 'POST':
        voice = Voice(voice=request.FILES['voice'])
        voice.save()

        # print(Voice.objects.all().last().voice.path)
        user_val = user_data(Voice.objects.all().last().voice.path)
        return home(request)
    return render(request, "karaoke.html", {'this_page': 'karaoke', 'state': "started", 'form': form})


def rec(request):
    print(request.POST)
    return render(request, "rec.html", {'this_page': 'rec', 'song_name_lst': df['Name'].to_list()})


def rec_res(request):
    print(request.POST)
    # print("val", )
    df_res = knn(user_val).head(10)
    df_res.set_index('Name', inplace=True)
    result_key = list(df_res['score_fq'].to_dict().keys())
    result_val = list(df_res['score_fq'].to_dict().values())

    song_note = {}

    for song in result_key:
        song_note[song] = df_res.loc[song].transpose().map(
            lambda x: x if x == 1 else None).dropna().to_dict().keys()
        song_note[song] = [i.split("_")[0] for i in song_note[song]]

    # print(song_note)

    user_song = {}

    for song, val in song_note.items():
        lst_cahce = []
        for i in val:
            lst_cahce.append(user_val[table_head.index(i)-1])
        user_song[song] = lst_cahce

    # print(user_song)

    max_user = [max(i) for i in user_song.values()]
    min_user = [min(i) for i in user_song.values()]

    avg_great_note = []
    avg_medium_note = []
    avg_bad_note = []

    len_great_note = []
    len_medium_note = []
    len_bad_note = []

    def avg(lst):
        if len(lst) <= 0:
            return 0
        return sum(lst)/len(lst)
    for song, val in user_song.items():
        avg_great_note.append(avg([i for i in val if i > 0.85]))
        avg_medium_note.append(avg([i for i in val if 0.7 < i <= 0.85]))
        avg_bad_note.append(avg([i for i in val if 0.5 <= i <= 0.7]))

        len_great_note.append(len([i for i in val if i > 0.85]))
        len_medium_note.append(len([i for i in val if 0.7 < i <= 0.85]))
        len_bad_note.append(len([i for i in val if 0.5 <= i <= 0.7]))

    return render(request, "rec-res.html", {'this_page': 'rec', 'table_head': table_head, 'table_content': zip(table_head[1:], user_val), 'result_key': result_key[0], 'result_val': result_val[0], 'result': zip(result_key[1:], result_val[1:]), 'result_max': max_user[0], 'result_min': min_user[0], 'result_avg_great': avg_great_note[0], 'result_avg_med': avg_medium_note[0], 'result_avg_bad': avg_bad_note[0], 'result_full': zip(result_key[1:], result_val[1:], max_user[1:], min_user[1:], avg_great_note[1:], avg_medium_note[1:], avg_bad_note[1:]), 'result_len': zip(result_key, len_great_note, len_medium_note, len_bad_note)})


def graph_js(request):
    df_res = knn(user_val).head(10)
    df_res.set_index('Name', inplace=True)
    result_key = list(df_res['score_fq'].to_dict().keys())
    result_val = list(df_res['score_fq'].to_dict().values())

    song_note = {}

    for song in result_key:
        song_note[song] = df_res.loc[song].transpose().map(
            lambda x: x if x == 1 else None).dropna().to_dict().keys()
        song_note[song] = [i.split("_")[0] for i in song_note[song]]

    # print(song_note)

    user_song = {}

    for song, val in song_note.items():
        lst_cahce = []
        for i in val:
            lst_cahce.append(user_val[table_head.index(i)-1])
        user_song[song] = lst_cahce

    # print(user_song)

    max_user = [max(i) for i in user_song.values()]
    min_user = [min(i) for i in user_song.values()]

    avg_great_note = []
    avg_medium_note = []
    avg_bad_note = []

    len_great_note = []
    len_medium_note = []
    len_bad_note = []

    def avg(lst):
        if len(lst) <= 0:
            return 0
        return sum(lst)/len(lst)
    for song, val in user_song.items():
        avg_great_note.append(avg([i for i in val if i > 0.85]))
        avg_medium_note.append(avg([i for i in val if 0.7 < i <= 0.85]))
        avg_bad_note.append(avg([i for i in val if 0.5 <= i <= 0.7]))

        len_great_note.append(len([i for i in val if i > 0.85]))
        len_medium_note.append(len([i for i in val if 0.7 < i <= 0.85]))
        len_bad_note.append(len([i for i in val if 0.5 <= i <= 0.7]))

    return render(request, 'graph.js', {'result_len': zip(result_key, len_great_note, len_medium_note, len_bad_note)})


def rec_res_explain(request):
    print(request.POST)
    # print(request.POST.values)

    user_new = [float(i[0]) for i in list(dict(request.POST).values())[1:]]

    print(user_new)

    df_res = knn(user_new).head(10)
    df_res.set_index('Name', inplace=True)
    result_key = list(df_res['score_fq'].to_dict().keys())
    result_val = list(df_res['score_fq'].to_dict().values())

    song_note = {}

    for song in result_key:
        song_note[song] = df_res.loc[song].transpose().map(
            lambda x: x if x == 1 else None).dropna().to_dict().keys()
        song_note[song] = [i.split("_")[0] for i in song_note[song]]

    # print(song_note)

    user_song = {}

    for song, val in song_note.items():
        lst_cahce = []
        for i in val:
            lst_cahce.append(user_new[table_head.index(i)-1])
        user_song[song] = lst_cahce

    # print(user_song)

    max_user = [max(i) for i in user_song.values()]
    min_user = [min(i) for i in user_song.values()]

    avg_great_note = []
    avg_medium_note = []
    avg_bad_note = []

    len_great_note = []
    len_medium_note = []
    len_bad_note = []
    for song, val in user_song.items():
        avg_great_note.append(
            sum([i for i in val if i > 0.85])/len([i for i in val if i > 0.85]))
        avg_medium_note.append(
            sum([i for i in val if 0.7 < i <= 0.85])/len([i for i in val if 0.7 < i <= 0.85]))
        avg_bad_note.append(
            sum([i for i in val if 0.5 <= i <= 0.7])/len([i for i in val if 0.5 <= i <= 0.7]) if len([i for i in val if 0.5 <= i <= 0.7]) > 0 else 1)

        len_great_note.append(len([i for i in val if i > 0.85]))
        len_medium_note.append(len([i for i in val if 0.7 < i <= 0.85]))
        len_bad_note.append(len([i for i in val if 0.5 <= i <= 0.7]))

    return render(request, "rec-res.html", {'this_page': 'rec', 'table_head': table_head, 'table_content': zip(table_head[1:], user_new), 'result_key': result_key[0], 'result_val': result_val[0], 'result': zip(result_key[1:], result_val[1:]), 'result_max': max_user[0], 'result_min': min_user[0], 'result_avg_great': avg_great_note[0], 'result_avg_med': avg_medium_note[0], 'result_avg_bad': avg_bad_note[0], 'result_full': zip(result_key[1:], result_val[1:], max_user[1:], min_user[1:], avg_great_note[1:], avg_medium_note[1:], avg_bad_note[1:]), 'result_len': zip(result_key, len_great_note, len_medium_note, len_bad_note)})


def table_res(request):
    print(request.POST)
    return render(request, "404.html", {'this_page': 'rec', 'table_head': table_head, 'table_content': user_val})
