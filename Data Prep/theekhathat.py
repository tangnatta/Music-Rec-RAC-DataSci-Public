from music21 import *
from scipy.fft import fft, fftfreq, rfft, rfftfreq
from scipy.io import wavfile
from PIL import Image, UnidentifiedImageError
import streamlit as st
import librosa
import librosa.display
import numpy as np
import tempfile
import os 
import io
import pyaudio
import wave
import soundfile as sf
from io import BytesIO
import streamlit.components.v1 as components
import time

def freq(file, start_time, end_time):

    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    dataToRead = data[int(start_time * sr / 1000) : int(end_time * sr / 1000) + 1]

    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)


    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    return freq


def detect_onset(file_path):
    x, sr = librosa.load(file_path)
    onset_frames = librosa.onset.onset_detect(x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    onset_times = librosa.frames_to_time(onset_frames)
    return onset_times


def convert2notes(audio):
    y,sr = librosa.load(audio)
    onset_env = librosa.onset.onset_strength(y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    timestamps = librosa.frames_to_time(onset_frames, sr=sr)

    onset_times = []
    for i in range (len(timestamps)):
        start_frame = librosa.time_to_frames(timestamps[i], sr=sr)
        end_frame = librosa.time_to_frames(timestamps[i+1] if i+1 < len(timestamps) else timestamps[-1], sr=sr)
        start_time = librosa.frames_to_time(start_frame, sr=sr)
        end_time = librosa.frames_to_time(end_frame, sr=sr)
        onset_times.append(start_time)

    fre2not = []

    for i in range(len(timestamps)-1):
    
        frequen = freq(audio, onset_times[i]*1000,onset_times[i+1]*1000)
        fre2not.append(frequen)

    librosa_note= []
    for i,fre in enumerate(fre2not):
        try:
            if fre == 0.0:
                librosa_note.append(librosa_note[i-1])
            if fre > 1371:
                librosa_note.append(librosa_note[i-1])
            else:
                a = librosa.hz_to_note(fre)
                librosa_note.append(a)
        except:
            if fre != 0.0:
                a = librosa.hz_to_note(fre)
                librosa_note.append(a)
    

    for idx, i in enumerate(librosa_note):
        a = i
        if len(i) == 3:
            k = []
            for x in a:
                x.split()
                k.append(x)

            k[1] = '#'
            new_note = "".join(k) 
            librosa_note[idx] = new_note

    Tempo, beats=librosa.beat.beat_track(y=y, sr=sr)
    Tempo=int(2*round(Tempo/2))

    durations = []

    for i in range(len(onset_times)-1):

        durations.append((onset_times[i+1]-onset_times[i])*Tempo/60)

    
    Note_sym = []
    for i in durations:
    
        Note_sym.append(i//4*4)
        i%=4

        Note_sym.append(i//2*2)
        i%=2
        

        Note_sym.append(i//1*1)
        i%=1
        
        Note_sym.append(i//0.5*0.5)
        i%=0.5

        Note_sym.append(i//0.25*0.25)
        i%=0.25

        Note_sym.append(i//0.125*0.125)
        i%=0.125

    np.array(Note_sym).shape

    k = [sum(Note_sym[i:i+6]) for i in range(len(Note_sym)) if (i+6)%6 == 0]


    key_all = {'A major' : ['A','B','C#','D','E','F#','G#'],
        'Bb major' : ['A#','C','D','D#','F','G','A'],
        'B major' : ['B','C#','D#','E','F#','G#','A#'],
        'C major' : ['C','D','E','F','G','A','B'],
        'Db major' : ['C#','D#','F','F#','G#','B#','C'],
        'D major' : ['D','E','F#','G','A','B','C#'],
        'Eb major' : ['D#','F','G','G#','A#','C','D'],
        'E major' : ['E','F#','G#','A','B','C#','D#'],
        'F major' : ['F','G','A','A#','C','D','E'],
        'Gb major' : ['F#','G#','A#','B','C#','D#','F'],
        'G major' : ['G','A','B','C','D','E','F#'],
        'Ab major' : ['G#','A#','C','C#','D#','F','G']  }
    
    key_check = {'A major' : 0,
        'Bb major' : 0,
        'B major' : 0,
        'C major' : 0,
        'Db major' : 0,
        'D major' : 0,
        'Eb major' : 0,
        'E major' : 0,
        'F major' : 0,
        'Gb major' : 0,
        'G major' : 0,
        'Ab major' : 0 }

    note_all = {
    'A': 0,
    'A#': 0,
    'B': 0,
    'C': 0,
    'C#': 0,
    'D': 0,
    'D#': 0,
    'E': 0,
    'F': 0,
    'F#': 0,
    'G': 0,
    'G#': 0
    }

    for i in librosa_note:
        if len(i) == 3:
            k = []
            for x in i:
                x.split()
                k.append(x)
                
            k[2] = ''
            new_note_ = "".join(k)
            note_all[new_note_]+=1

        if len(i) == 2:
            k = []
            for x in i:
                x.split()
                k.append(x)
                
            k[1] = ''
            new_note_ = "".join(k)   
            note_all[new_note_]+=1 

    sorted_note = sorted(note_all.items(), key=lambda x:x[1], reverse=True)
    converted_note = dict(sorted_note)

    detect_key = list(converted_note.keys())[:7]

    for i in detect_key:
        try:
            if i == 'A': del key_all['B major']
            if i == 'A#': del key_all['C major']
            if i == 'B': del key_all['Db major']
            if i == 'C': del key_all['D major']
            if i == 'C#': del key_all['Eb major']
            if i == 'D': del key_all['E major']
            if i == 'D#': del key_all['F major']
            if i == 'E': del key_all['Gb major']
            if i == 'F': del key_all['G major']
            if i == 'F#': del key_all['Ab major']
            if i == 'G': del key_all['A major']
            if i == 'G#': del key_all['Bb major']
            if i == 'F': del key_all['B major']
            if i == 'F#': del key_all['C major']
            if i == 'G': del key_all['Db major']
            if i == 'G#': del key_all['D major']
            if i == 'A': del key_all['Eb major']
            if i == 'A#': del key_all['E major']
            if i == 'B': del key_all['F major']
            if i == 'C': del key_all['Gb major']
            if i == 'C#': del key_all['G major']
            if i == 'D': del key_all['Ab major']
            if i == 'D#': del key_all['A major']
            if i == 'E': del key_all['Bb major']

        except:
            pass
    
    if detect_key.count('A#') == 0:
        if list(key_all.keys()).count('B major') != 0: del key_all['B major']
        if list(key_all.keys()).count('F major') != 0: del key_all['F major']

    if detect_key.count('D#') == 0: 
        if list(key_all.keys()).count('Bb major') != 0: del key_all['Bb major']
        if list(key_all.keys()).count('E major') != 0: del key_all['E major']

    if detect_key.count('G#') == 0: 
        if list(key_all.keys()).count('Eb major') != 0: del key_all['Eb major']
        if list(key_all.keys()).count('A major') != 0: del key_all['A major']


    if detect_key.count('C#') == 0: 
        if list(key_all.keys()).count('Ab major') != 0: del key_all['Ab major']
        if list(key_all.keys()).count('D major') != 0: del key_all['D major']


    if detect_key.count('F#') == 0: 
        if list(key_all.keys()).count('Db major') != 0: del key_all['Db major']
        if list(key_all.keys()).count('G major') != 0: del key_all['G major']


    if detect_key.count('B') == 0: 
        if list(key_all.keys()).count('Gb major') != 0: del key_all['Gb major']

    if detect_key.count('F') == 0:
        if list(key_all.keys()).count('F# major') != 0: del key_all['F# major']

    
    for k in list(key_all.keys()):
        for note_key in key_all[k]:
            for note_ in detect_key:
                if note_key == note_:
                    key_check[k]+=1


    sorted_key = sorted(key_check.items(), key=lambda x:x[1], reverse=True)
    converted_key = dict(sorted_key)

    Key = list(converted_key.keys())[0]

    Note_sym_real = [sum(Note_sym[i:i+6]) for i in range(len(Note_sym)) if (i+6)%6 == 0]

    Note_sym_real_real = [ i/0.125 for i in Note_sym_real]

    note_with_du_4 = []
    current_note = []
    current_duration = 0
    k=0

    for i in range(len(librosa_note)):
        k+=1
        if current_duration < 32:
            current_duration += Note_sym_real_real[i]
            if  current_duration > 32:
                current_note.append(librosa_note[i])
                note_with_du_4.append(current_note)
                current_note = [librosa_note[i]]
                current_duration -= 32
            
            else:
                current_note.append(librosa_note[i])

        if current_duration > 32:
            n = current_duration - 32
    
            if n > 32:
                current_note.append(librosa_note[i])
                note_with_du_4.append(current_note)
                m = n//32
                l = n - m*32
                for _ in range(int(m)):
                    note_with_du_4.append(librosa_note[i])
                current_duration = l
                current_note = [librosa_note[i]]

            if n < 32:
                current_note.append(librosa_note[i])
                note_with_du_4.append(current_note)
                current_duration = n
                current_note = [librosa_note[i]]
                

            if n == 32:
                current_note.append(librosa_note[i])
                note_with_du_4.append(current_note)
                note_with_du_4.append(librosa_note[i])
                current_duration = 0
                current_note = []

        if current_duration == 32:
            current_note.append(librosa_note[i])
            note_with_du_4.append(current_note)
            current_duration = 0
            current_note = []

    chord_dict_plus = {
        "C": ["C3", "E3", "G3"],
        "Cm": ["C3", "D#3", "G3"],
        "C#": ["C#3", "F3", "G#3"],
        "C#m": ["C#3", "E3", "G#3"],
        "D": ["D3", "F#3", "A3"],
        "Dm": ["D3", "F3", "A3"],
        "D#": ["D#3", "G3", "A#3"],
        "D#m": ["D#3", "F#3", "A#3"],
        "E": ["E3", "G#3", "B3"],
        "Em": ["E3", "G3", "B3"],
        "F": ["F3", "A3", "C3"],
        "Fm": ["F3", "G#3", "C3"],
        "F#": ["F#3", "A#3", "C#3"],
        "F#m": ["F#3", "A3", "C#3"],
        "G": ["G3", "B3", "D3"],
        "Gm": ["G3", "A#3", "D3"],
        "G#": ["G#3", "C3", "D#3"],
        "G#m": ["G#3", "B3", "D#3"],
        "A": ["A3", "C#3", "E3"],
        "Am": ["A3", "C3", "E3"],
        "A#": ["A#3", "D3", "F3"],
        "A#m": ["A#3", "C#3", "F3"],
        "B": ["B3", "D#3", "F#3"],
        "Bm": ["B3", "D3", "F#3"]
    }

    chord_dict_minus = {
        "C": ["C3", "E3", "G3"],
        "Cm": ["C3", "Eb3", "G3"],
        "C#": ["Db3", "F3", "Ab3"],
        "C#m": ["C#3", "E3", "G#3"],
        "D": ["D3", "F#3", "A3"],
        "Dm": ["D3", "F3", "A3"],
        "D#": ["Eb3", "G3", "Bb3"],
        "D#m": ["Eb3", "Gb3", "Bb3"],
        "E": ["E3", "G#3", "B3"],
        "Em": ["E3", "G3", "B3"],
        "F": ["F3", "A3", "C3"],
        "Fm": ["F3", "Ab3", "C3"],
        "F#": ["Gb3", "Bb3", "Db3"],
        "F#m": ["F#3", "A3", "C#3"],
        "G": ["G3", "B3", "D3"],
        "Gm": ["G3", "Bb3", "D3"],
        "G#": ["Ab3", "C3", "Eb3"],
        "G#m": ["G#3", "B3", "D#3"],
        "A": ["A3", "C#3", "E3"],
        "Am": ["A3", "C3", "E3"],
        "A#": ["Bb3", "D3", "F3"],
        "A#m": ["Bb3", "Db3", "F3"],
        "B": ["B3", "D#3", "F#3"],
        "Bm": ["B3", "D3", "F#3"]
    }

    KeydelC = {  'A major': ['A', 'Bm', 'C#m', 'C#', 'D', 'E', 'F#m'],
            'Bb major': ['A#', 'Cm', 'Dm', 'D', 'D#', 'F', 'Gm'],
            'B major': ['B', 'C#m', 'D#m', 'D#', 'E', 'F#', 'G#m'],
            'C major': ['C', 'Dm', 'Em', 'E', 'F', 'G', 'Am'],
            'Db major': ['C#', 'D#m', 'Fm', 'F', 'F#', 'G#', 'A#m'],
            'D major': ['D', 'Em', 'F#m', 'F#', 'G', 'A', 'Bm'],
            'Eb major':['D#', 'Fm', 'Gm', 'G', 'G#', 'A#', 'Cm'],
            'E major': ['E', 'F#m', 'G#m', 'G#', 'A', 'B', 'C#m'],
            'F major': ['F', 'Gm', 'Am', 'A', 'A#', 'C', 'Dm'],
            'Gb major':['F#', 'G#m', 'A#m', 'A#', 'B', 'C#', 'D#m'],
            'G major': ['G', 'Am', 'Bm', 'B', 'C', 'D', 'Em'],
            'Ab major': ['G#', 'A#m', 'Cm', 'C', 'C#', 'D#', 'Fm']
        }   
    
    key2num = { 'B major' : 5, 
            'E major' : 4,
            'A major' : 3,
            'D major' : 2,
            'G major' : 1,
            'C major' : 0,
            'F major' : -1,
            'Bb major' : -2,
            'Eb major' : -3,
            'Ab major' : -4,
            'Db major' : -5,
            'Gb major' : -6,        
        }
    
    if key2num[Key] >= 0:
        new_chord_dict = {}
        for i in KeydelC[Key]:
            new_chord_dict[i] = chord_dict_plus[i]

    else:
        new_chord_dict = {}
        for i in KeydelC[Key]:
            new_chord_dict[i] = chord_dict_minus[i]

    real_chord = []
    choose_chord = []
    for i in note_with_du_4 :
        for k in new_chord_dict:
            choose_chord.append(len(list(set(i) & set(new_chord_dict[k]))))

        for i, num in enumerate(choose_chord):
            if num == max(choose_chord):
                real_chord.append(new_chord_dict[list(new_chord_dict)[i]])
                break
        choose_chord = []
    
    librosa_note_flat=[]
    if key2num[Key] < 0:
        for i in range(len(librosa_note)):
            if librosa_note[i][1] == '#':
                flatnote=librosa_note[i][0] + "b" + librosa_note[i][2]
                
                if flatnote[0]=='C':
                    flatnote='D'+flatnote[1:]
                elif flatnote[0]=='D':
                    flatnote='E'+flatnote[1:]
                elif flatnote[0]=='F':
                    flatnote='G'+flatnote[1:]
                elif flatnote[0]=='G':
                    flatnote='A'+flatnote[1:]
                elif flatnote[0]=='A':
                    flatnote='B'+flatnote[1:]

                librosa_note_flat.append(flatnote)
            
            else:
                librosa_note_flat.append(librosa_note[i])
    
        librosa_note=librosa_note_flat

    us = environment.UserSettings()
    us['musicxmlPath'] = r'C://Program Files//MuseScore 3//bin//MuseScore3.exe'
    us['musescoreDirectPNGPath'] = r'C://Program Files//MuseScore 3//bin//MuseScore3.exe'
    us['lilypondPath'] = r'C://Users//UNS_CT//Downloads//lilypond-2.24.1-mingw-x86_64//lilypond-2.24.1//bin//lilypond.exe'

    score = stream.Score()
    upper_staff = stream.Part()
    lower_staff = stream.Part()
    score.insert(0, upper_staff)
    score.insert(0, lower_staff)

    ks_upper = key.KeySignature(key2num[Key])  
    upper_staff.append(ks_upper)

    ks_lower = key.KeySignature(key2num[Key]) 
    lower_staff.append(ks_lower)
    lower_staff.clef = clef.FClef()

    for i, pitch in enumerate(librosa_note):
        upper_staff.append([note.Note(librosa_note[i], quarterLength=Note_sym_real[i])])

    for i in real_chord:
        chord_obj = chord.Chord(i)
        chord_obj.duration = duration.Duration(4.0)  
        lower_staff.append(chord_obj) 


    with tempfile.NamedTemporaryFile(suffix='.musicxml', delete=False) as f:
        score.write()
        filename = os.listdir('C:/Users/UNS_CT/AppData/Local/Temp/music21')
        
    try:
        for i in range(len(filename)):
            if (os.listdir('C:/Users/UNS_CT/AppData/Local/Temp/music21'))[i][-1] == 'l':
                score_ = converter.parse('C:/Users/UNS_CT/AppData/Local/Temp/music21/'+filename[i])
                image = Image.open(score_.write('musicxml.png', 'png') )
                st.image(image, use_column_width=True)
    except:
        print(filename)

    for i in range(len(filename)):
        os.remove('C:/Users/UNS_CT/AppData/Local/Temp/music21/'+filename[i])
    os.remove(audio)


def count_time():
    
    if "start_time" not in st.session_state and st.session_state.get("button_clicked", False):
        st.session_state.start_time = time.time()
        st.session_state.button_label = "Click to Stop"
    elif "start_time" in st.session_state:
        elapsed_time = time.time() - st.session_state.start_time
        st.session_state.last_elapsed_time = elapsed_time
        st.session_state.button_label = "Click to Start Again"
        del st.session_state.start_time

    if st.button(st.session_state.get("button_label", "Click to Start")):
        st.session_state.button_clicked = True
        count_time()



def main():
 
 try:
    st.title("Music2Notes")
    st.markdown("<br>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Audio", type=["wav"])
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 14.5px;'>Record Audio</p>", unsafe_allow_html=True) 
    
    # if st.button('Start Recording'):
  
    #     # st.write("Please enter the duration of the recording in seconds:")
    #     # record_seconds = 0
    #     # counter_stop = 1
    #     # while record_seconds == 0:
    #     #     record_seconds = st.number_input("Enter the duration of the recording in seconds:", min_value=0, max_value=3600, key=f"record_seconds_input-{counter_stop}")
    #     #     counter_stop += 1
            
    #     # if record_seconds != 0:
             
    #     #     FORMAT = pyaudio.paInt16
    #     #     CHANNELS = 1
    #     #     RATE = 44100
    #     #     CHUNK = 1024

    #     #     print(record_seconds)
    #     #     p = pyaudio.PyAudio()

    #     #     stream = p.open(format=FORMAT, channels=CHANNELS,
    #     #                 rate=RATE, input=True,
    #     #                 frames_per_buffer=CHUNK)
    #     #     frames = []

    #     #     for i in range(0, int(RATE / CHUNK * record_seconds)):
    #     #         data = stream.read(CHUNK)
    #     #         frames.append(data)

    #     #     stream.stop_stream()
    #     #     stream.close()
    #     #     p.terminate()

    #     #     wf = wave.open("output.wav", "wb")
    #     #     wf.setnchannels(CHANNELS)
    #     #     wf.setsampwidth(p.get_sample_size(FORMAT))
    #     #     wf.setframerate(RATE)
    #     #     wf.writeframes(b"".join(frames))
    #     #     wf.close()
    #     #     convert2notes("output.wav")
    #         pass

    count_time()

    if "last_elapsed_time" in st.session_state:
        st.write("Last elapsed time:", round(st.session_state.last_elapsed_time, 2))
        print(round(st.session_state.last_elapsed_time, 2))


    if uploaded_file is not None:

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_filename = tmp_file.name

    
        with open(tmp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        y,sr = librosa.load(tmp_filename)
        onset_env = librosa.onset.onset_strength(y, sr=sr)
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        timestamps = librosa.frames_to_time(onset_frames, sr=sr)

        onset_times = []
        for i in range (len(timestamps)):
            start_frame = librosa.time_to_frames(timestamps[i], sr=sr)
            end_frame = librosa.time_to_frames(timestamps[i+1] if i+1 < len(timestamps) else timestamps[-1], sr=sr)
            start_time = librosa.frames_to_time(start_frame, sr=sr)
            end_time = librosa.frames_to_time(end_frame, sr=sr)
            onset_times.append(start_time)

        fre2not = []

        for i in range(len(timestamps)-1):
        
            frequen = freq(uploaded_file, onset_times[i]*1000,onset_times[i+1]*1000)
            fre2not.append(frequen)

        librosa_note= []
        for i,fre in enumerate(fre2not):
            try:
                if fre == 0.0:
                    librosa_note.append(librosa_note[i-1])
                if fre > 1371:
                    librosa_note.append(librosa_note[i-1])
                else:
                    a = librosa.hz_to_note(fre)
                    librosa_note.append(a)
            except:
                if fre != 0.0:
                    a = librosa.hz_to_note(fre)
                    librosa_note.append(a)
        

        for idx, i in enumerate(librosa_note):
            a = i
            if len(i) == 3:
                k = []
                for x in a:
                    x.split()
                    k.append(x)

                k[1] = '#'
                new_note = "".join(k) 
                librosa_note[idx] = new_note
    
        Tempo, beats=librosa.beat.beat_track(y=y, sr=sr)
        Tempo=int(2*round(Tempo/2))

        durations = []

        for i in range(len(onset_times)-1):

            durations.append((onset_times[i+1]-onset_times[i])*Tempo/60)

        
        Note_sym = []
        for i in durations:
        
            Note_sym.append(i//4*4)
            i%=4

            Note_sym.append(i//2*2)
            i%=2
            

            Note_sym.append(i//1*1)
            i%=1
            
            Note_sym.append(i//0.5*0.5)
            i%=0.5

            Note_sym.append(i//0.25*0.25)
            i%=0.25

            Note_sym.append(i//0.125*0.125)
            i%=0.125

        np.array(Note_sym).shape

        k = [sum(Note_sym[i:i+6]) for i in range(len(Note_sym)) if (i+6)%6 == 0]


        key_all = {'A major' : ['A','B','C#','D','E','F#','G#'],
            'Bb major' : ['A#','C','D','D#','F','G','A'],
            'B major' : ['B','C#','D#','E','F#','G#','A#'],
            'C major' : ['C','D','E','F','G','A','B'],
            'Db major' : ['C#','D#','F','F#','G#','B#','C'],
            'D major' : ['D','E','F#','G','A','B','C#'],
            'Eb major' : ['D#','F','G','G#','A#','C','D'],
            'E major' : ['E','F#','G#','A','B','C#','D#'],
            'F major' : ['F','G','A','A#','C','D','E'],
            'Gb major' : ['F#','G#','A#','B','C#','D#','F'],
            'G major' : ['G','A','B','C','D','E','F#'],
            'Ab major' : ['G#','A#','C','C#','D#','F','G']  }
        
        key_check = {'A major' : 0,
            'Bb major' : 0,
            'B major' : 0,
            'C major' : 0,
            'Db major' : 0,
            'D major' : 0,
            'Eb major' : 0,
            'E major' : 0,
            'F major' : 0,
            'Gb major' : 0,
            'G major' : 0,
            'Ab major' : 0 }

        note_all = {
        'A': 0,
        'A#': 0,
        'B': 0,
        'C': 0,
        'C#': 0,
        'D': 0,
        'D#': 0,
        'E': 0,
        'F': 0,
        'F#': 0,
        'G': 0,
        'G#': 0
        }

        for i in librosa_note:
            if len(i) == 3:
                k = []
                for x in i:
                    x.split()
                    k.append(x)
                    
                k[2] = ''
                new_note_ = "".join(k)
                note_all[new_note_]+=1

            if len(i) == 2:
                k = []
                for x in i:
                    x.split()
                    k.append(x)
                    
                k[1] = ''
                new_note_ = "".join(k)   
                note_all[new_note_]+=1 

        sorted_note = sorted(note_all.items(), key=lambda x:x[1], reverse=True)
        converted_note = dict(sorted_note)

        detect_key = list(converted_note.keys())[:7]

        for i in detect_key:
            try:
                if i == 'A': del key_all['B major']
                if i == 'A#': del key_all['C major']
                if i == 'B': del key_all['Db major']
                if i == 'C': del key_all['D major']
                if i == 'C#': del key_all['Eb major']
                if i == 'D': del key_all['E major']
                if i == 'D#': del key_all['F major']
                if i == 'E': del key_all['Gb major']
                if i == 'F': del key_all['G major']
                if i == 'F#': del key_all['Ab major']
                if i == 'G': del key_all['A major']
                if i == 'G#': del key_all['Bb major']
                if i == 'F': del key_all['B major']
                if i == 'F#': del key_all['C major']
                if i == 'G': del key_all['Db major']
                if i == 'G#': del key_all['D major']
                if i == 'A': del key_all['Eb major']
                if i == 'A#': del key_all['E major']
                if i == 'B': del key_all['F major']
                if i == 'C': del key_all['Gb major']
                if i == 'C#': del key_all['G major']
                if i == 'D': del key_all['Ab major']
                if i == 'D#': del key_all['A major']
                if i == 'E': del key_all['Bb major']

            except:
                pass
        
        if detect_key.count('A#') == 0:
            if list(key_all.keys()).count('B major') != 0: del key_all['B major']
            if list(key_all.keys()).count('F major') != 0: del key_all['F major']

        if detect_key.count('D#') == 0: 
            if list(key_all.keys()).count('Bb major') != 0: del key_all['Bb major']
            if list(key_all.keys()).count('E major') != 0: del key_all['E major']

        if detect_key.count('G#') == 0: 
            if list(key_all.keys()).count('Eb major') != 0: del key_all['Eb major']
            if list(key_all.keys()).count('A major') != 0: del key_all['A major']


        if detect_key.count('C#') == 0: 
            if list(key_all.keys()).count('Ab major') != 0: del key_all['Ab major']
            if list(key_all.keys()).count('D major') != 0: del key_all['D major']


        if detect_key.count('F#') == 0: 
            if list(key_all.keys()).count('Db major') != 0: del key_all['Db major']
            if list(key_all.keys()).count('G major') != 0: del key_all['G major']


        if detect_key.count('B') == 0: 
            if list(key_all.keys()).count('Gb major') != 0: del key_all['Gb major']

        if detect_key.count('F') == 0:
            if list(key_all.keys()).count('F# major') != 0: del key_all['F# major']

        
        for k in list(key_all.keys()):
            for note_key in key_all[k]:
                for note_ in detect_key:
                    if note_key == note_:
                        key_check[k]+=1


        sorted_key = sorted(key_check.items(), key=lambda x:x[1], reverse=True)
        converted_key = dict(sorted_key)

        Key = list(converted_key.keys())[0]

        Note_sym_real = [sum(Note_sym[i:i+6]) for i in range(len(Note_sym)) if (i+6)%6 == 0]

        Note_sym_real_real = [ i/0.125 for i in Note_sym_real]

        note_with_du_4 = []
        current_note = []
        current_duration = 0
        k=0

        for i in range(len(librosa_note)):
            k+=1
            if current_duration < 32:
                current_duration += Note_sym_real_real[i]
                if  current_duration > 32:
                    current_note.append(librosa_note[i])
                    note_with_du_4.append(current_note)
                    current_note = [librosa_note[i]]
                    current_duration -= 32
                
                else:
                    current_note.append(librosa_note[i])

            if current_duration > 32:
                n = current_duration - 32
        
                if n > 32:
                    current_note.append(librosa_note[i])
                    note_with_du_4.append(current_note)
                    m = n//32
                    l = n - m*32
                    for _ in range(int(m)):
                        note_with_du_4.append(librosa_note[i])
                    current_duration = l
                    current_note = [librosa_note[i]]

                if n < 32:
                    current_note.append(librosa_note[i])
                    note_with_du_4.append(current_note)
                    current_duration = n
                    current_note = [librosa_note[i]]
                    

                if n == 32:
                    current_note.append(librosa_note[i])
                    note_with_du_4.append(current_note)
                    note_with_du_4.append(librosa_note[i])
                    current_duration = 0
                    current_note = []

            if current_duration == 32:
                current_note.append(librosa_note[i])
                note_with_du_4.append(current_note)
                current_duration = 0
                current_note = []

        chord_dict_plus = {
            "C": ["C3", "E3", "G3"],
            "Cm": ["C3", "D#3", "G3"],
            "C#": ["C#3", "F3", "G#3"],
            "C#m": ["C#3", "E3", "G#3"],
            "D": ["D3", "F#3", "A3"],
            "Dm": ["D3", "F3", "A3"],
            "D#": ["D#3", "G3", "A#3"],
            "D#m": ["D#3", "F#3", "A#3"],
            "E": ["E3", "G#3", "B3"],
            "Em": ["E3", "G3", "B3"],
            "F": ["F3", "A3", "C3"],
            "Fm": ["F3", "G#3", "C3"],
            "F#": ["F#3", "A#3", "C#3"],
            "F#m": ["F#3", "A3", "C#3"],
            "G": ["G3", "B3", "D3"],
            "Gm": ["G3", "A#3", "D3"],
            "G#": ["G#3", "C3", "D#3"],
            "G#m": ["G#3", "B3", "D#3"],
            "A": ["A3", "C#3", "E3"],
            "Am": ["A3", "C3", "E3"],
            "A#": ["A#3", "D3", "F3"],
            "A#m": ["A#3", "C#3", "F3"],
            "B": ["B3", "D#3", "F#3"],
            "Bm": ["B3", "D3", "F#3"]
        }

        chord_dict_minus = {
            "C": ["C3", "E3", "G3"],
            "Cm": ["C3", "Eb3", "G3"],
            "C#": ["Db3", "F3", "Ab3"],
            "C#m": ["C#3", "E3", "G#3"],
            "D": ["D3", "F#3", "A3"],
            "Dm": ["D3", "F3", "A3"],
            "D#": ["Eb3", "G3", "Bb3"],
            "D#m": ["Eb3", "Gb3", "Bb3"],
            "E": ["E3", "G#3", "B3"],
            "Em": ["E3", "G3", "B3"],
            "F": ["F3", "A3", "C3"],
            "Fm": ["F3", "Ab3", "C3"],
            "F#": ["Gb3", "Bb3", "Db3"],
            "F#m": ["F#3", "A3", "C#3"],
            "G": ["G3", "B3", "D3"],
            "Gm": ["G3", "Bb3", "D3"],
            "G#": ["Ab3", "C3", "Eb3"],
            "G#m": ["G#3", "B3", "D#3"],
            "A": ["A3", "C#3", "E3"],
            "Am": ["A3", "C3", "E3"],
            "A#": ["Bb3", "D3", "F3"],
            "A#m": ["Bb3", "Db3", "F3"],
            "B": ["B3", "D#3", "F#3"],
            "Bm": ["B3", "D3", "F#3"]
        }

        KeydelC = {  'A major': ['A', 'Bm', 'C#m', 'C#', 'D', 'E', 'F#m'],
                'Bb major': ['A#', 'Cm', 'Dm', 'D', 'D#', 'F', 'Gm'],
                'B major': ['B', 'C#m', 'D#m', 'D#', 'E', 'F#', 'G#m'],
                'C major': ['C', 'Dm', 'Em', 'E', 'F', 'G', 'Am'],
                'Db major': ['C#', 'D#m', 'Fm', 'F', 'F#', 'G#', 'A#m'],
                'D major': ['D', 'Em', 'F#m', 'F#', 'G', 'A', 'Bm'],
                'Eb major':['D#', 'Fm', 'Gm', 'G', 'G#', 'A#', 'Cm'],
                'E major': ['E', 'F#m', 'G#m', 'G#', 'A', 'B', 'C#m'],
                'F major': ['F', 'Gm', 'Am', 'A', 'A#', 'C', 'Dm'],
                'Gb major':['F#', 'G#m', 'A#m', 'A#', 'B', 'C#', 'D#m'],
                'G major': ['G', 'Am', 'Bm', 'B', 'C', 'D', 'Em'],
                'Ab major': ['G#', 'A#m', 'Cm', 'C', 'C#', 'D#', 'Fm']
            }   
        
        key2num = { 'B major' : 5, 
                'E major' : 4,
                'A major' : 3,
                'D major' : 2,
                'G major' : 1,
                'C major' : 0,
                'F major' : -1,
                'Bb major' : -2,
                'Eb major' : -3,
                'Ab major' : -4,
                'Db major' : -5,
                'Gb major' : -6,        
            }
        
        if key2num[Key] >= 0:
            new_chord_dict = {}
            for i in KeydelC[Key]:
                new_chord_dict[i] = chord_dict_plus[i]

        else:
            new_chord_dict = {}
            for i in KeydelC[Key]:
                new_chord_dict[i] = chord_dict_minus[i]

        real_chord = []
        choose_chord = []
        for i in note_with_du_4 :
            for k in new_chord_dict:
                choose_chord.append(len(list(set(i) & set(new_chord_dict[k]))))

            for i, num in enumerate(choose_chord):
                if num == max(choose_chord):
                    real_chord.append(new_chord_dict[list(new_chord_dict)[i]])
                    break
            choose_chord = []
        
        librosa_note_flat=[]
        if key2num[Key] < 0:
            for i in range(len(librosa_note)):
                if librosa_note[i][1] == '#':
                    flatnote=librosa_note[i][0] + "b" + librosa_note[i][2]
                    
                    if flatnote[0]=='C':
                        flatnote='D'+flatnote[1:]
                    elif flatnote[0]=='D':
                        flatnote='E'+flatnote[1:]
                    elif flatnote[0]=='F':
                        flatnote='G'+flatnote[1:]
                    elif flatnote[0]=='G':
                        flatnote='A'+flatnote[1:]
                    elif flatnote[0]=='A':
                        flatnote='B'+flatnote[1:]

                    librosa_note_flat.append(flatnote)
                
                else:
                    librosa_note_flat.append(librosa_note[i])
        
            librosa_note=librosa_note_flat

        us = environment.UserSettings()
        us['musicxmlPath'] = r'C://Program Files//MuseScore 3//bin//MuseScore3.exe'
        us['musescoreDirectPNGPath'] = r'C://Program Files//MuseScore 3//bin//MuseScore3.exe'
        us['lilypondPath'] = r'C://Users//UNS_CT//Downloads//lilypond-2.24.1-mingw-x86_64//lilypond-2.24.1//bin//lilypond.exe'

        score = stream.Score()
        upper_staff = stream.Part()
        lower_staff = stream.Part()
        score.insert(0, upper_staff)
        score.insert(0, lower_staff)

        ks_upper = key.KeySignature(key2num[Key])  
        upper_staff.append(ks_upper)

        ks_lower = key.KeySignature(key2num[Key]) 
        lower_staff.append(ks_lower)
        lower_staff.clef = clef.FClef()

        for i, pitch in enumerate(librosa_note):
            upper_staff.append([note.Note(librosa_note[i], quarterLength=Note_sym_real[i])])

        for i in real_chord:
            chord_obj = chord.Chord(i)
            chord_obj.duration = duration.Duration(4.0)  
            lower_staff.append(chord_obj) 


        with tempfile.NamedTemporaryFile(suffix='.musicxml', delete=False) as f:
            score.write()
            filename = os.listdir('C:/Users/UNS_CT/AppData/Local/Temp/music21')
            
        try:
            for i in range(len(filename)):
                if (os.listdir('C:/Users/UNS_CT/AppData/Local/Temp/music21'))[i][-1] == 'l':
                    score_ = converter.parse('C:/Users/UNS_CT/AppData/Local/Temp/music21/'+filename[i])
                    image = Image.open(score_.write('musicxml.png', 'png') )
                    st.image(image, use_column_width=True)
        except:
            print(filename)

        for i in range(len(filename)):
            os.remove('C:/Users/UNS_CT/AppData/Local/Temp/music21/'+filename[i])
        os.remove(tmp_filename)
 
 except:
      st.markdown("<p style='font-size: 15px; color: red;'>Please refresh and try again</p>", unsafe_allow_html=True) 

if __name__ == "__main__":
  main()