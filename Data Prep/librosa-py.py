import librosa
import numpy as np
from scipy.fft import fft, fftfreq, rfft, rfftfreq
import pandas as pd

AUDIO = "D:\\Github\\Music-Rec-RAC-DataSci\\วงวน - SERIOUS BACON ( ORIGINAL by ONEONE )\\vocals.mp3"

y, sr = librosa.load(AUDIO)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env)
timestamps = librosa.frames_to_time(onset_frames, sr=sr)

print("onset_env", onset_env)
print("onset_frames",onset_frames)
print("timestamps",timestamps)

data_dic = []

for i, onset_frame in enumerate(onset_frames):
    start_time = librosa.frames_to_time(onset_frame, sr=sr)
    end_time = librosa.frames_to_time(onset_frames[i+1] if i+1 < len(timestamps) else onset_frames[-1], sr=sr)
    
    # print("start_time", start_time)
    # print("end_time", end_time)
    
    dataToRead = y[int(start_time * sr) : int(end_time * sr) + 1]

    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / sr)
    
    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    
    data_dic.append({
        "start_time": start_time,
        "end_time": end_time,
        "freq": freq
    })
    
df = pd.DataFrame(data_dic[:-1])
print(df)