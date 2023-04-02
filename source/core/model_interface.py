#####
# Record audio
# Pass audio into model
# Pull output from model
# 
#####

import time
import pathlib
import sounddevice as sd
from scipy.io.wavfile import write
from scipy.io import wavfile
import tensorflow as tf
import numpy as np
import noisereduce as nr
from source.core.asr_module import pullKeywords
from source.core.asr_module import pullCharacters

# Create an array of the keywords which the model understands
keywords = pullKeywords('data/mini_speech_commands')
for word in keywords:
    print()
    print(keywords)

# Create a character array of the first letter of the keywords
ch_keywords = pullCharacters(keywords)
for character in keywords:
    print()
    print(character)

# Load the saved model
sherpa_asr = tf.saved_model.load('saved')

# Set the path for recording
audio_path = "data/output.wav"

# A function for recording a 1 second clip of audio
def Record():
    seconds = 1
    sampleRate = 16000
    print('...Recording in 3\n')
    time.sleep(1)      
    print('...Recording in 2\n')
    time.sleep(1)
    print('...Recording in 1\n')
    time.sleep(1)
    print('Go \n')
    time.sleep(0.5)

    #####
    # sd.rec (frames=None, samplerate=None, channels=None, dtype=None, out=None, mapping=None, blocking=False, **kwargs)
    # frames: number of frames to record
    # samplerate: the number of samples per second (or per other unit) taken from a continuous signal to make a discrete or digital signal
    #      -> the most common sampling rate is 44.1 kHz (which is 44,100 samples of audio per second)
    # channels: number of channels to record
    # dtype: datatype of the recording
    #
    # myRecording becomes a numpy.ndarray – The recorded data.
    #####

    myRecording = sd.rec(int(seconds * sampleRate), samplerate=sampleRate, channels=1, dtype = np.int16)
    sd.wait()  # Wait until recording is finished

    #####
    # scipy.io.wavfile.write(filename, rate, data)
    #####
    write(audio_path, sampleRate, myRecording)

    rate, data = wavfile.read("data/output.wav")

    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write("data/output.wav", rate, reduced_noise)

    print("Successfully Recorded.")
    return None


def use_model(audio_path):
    fin = sherpa_asr(tf.constant(str(audio_path)))
    run_up = fin['predictions'].numpy()
    print("run up: ")
    print(run_up)
    out = np.array2string(fin['class_names'].numpy())
    print("out: ")
    print(out)
    return run_up, out

#Pull the answer and index from pred list
def veri_n_ind(out):
    for i in range(len(chKeywords)):
        print("i: ", i)
        print("keywords[i]: ", chKeywords[i])

        if out[3] == chKeywords[i]:
            count = i
            ans = chKeywords[i]

    return count, ans

