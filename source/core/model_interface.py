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
import soundfile as sf

# Create an array of the keywords which the model understands
keywords = ['down', 'go', 'left', 'no', 'right', 'stop', 'up', 'yes']

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
    time.sleep(0.3)

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

    myRecording = sd.rec(int(seconds * sampleRate), samplerate=sampleRate, channels=1, dtype = np.float64)
    sd.wait()  # Wait until recording is finished

    #####
    # scipy.io.wavfile.write(filename, rate, data)
    #####
    write(audio_path, sampleRate, myRecording)

    rate, data = wavfile.read("data/output.wav")

    # perform noise reduction
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write("data/output.wav", rate, reduced_noise)

    return None

def use_model(audio_path):
    modelOutput = sherpa_asr(tf.constant(str(audio_path)))
#    print("modelOutput: ", modelOutput)

    confidenceValues = modelOutput['predictions'].numpy()
#    print("confidenceValues: ", confidenceValues)

    greatestPrediction = np.array2string(modelOutput['class_names'].numpy())
#    print("greatestPrediction: ", greatestPrediction)

    formattedGreatestPrediction = greatestPrediction.split("'")
    formattedGreatestPrediction = formattedGreatestPrediction[1]
#    print("formattedGreatestPrediciton: ", formattedGreatestPrediction)

    return confidenceValues, formattedGreatestPrediction


def checkPredictionWithUser(predictionToCheck):
    print("We heard: ", predictionToCheck)
    print("Is this the command you desire?")

    Record()
    confidenceValues, greatestPrediction = use_model(audio_path)

    if (greatestPrediction == "no"):
        return 0
    elif (greatestPrediction == "yes"):
        return 1
    else:
        return 2


