import time
import sounddevice as sd
from scipy.io.wavfile import write
import tensorflow as tf
import numpy as np
from command_module import *

# Create an array of the keywords which the model can understand
keywords = ['down','go', 'left', 'no', 'right', 'stop', 'up', 'yes']
chKeywords = ['d', 'g',  'l',    'n',  'r',      's',   'u',  'y']

# Load the saved model
sherpa_asr = tf.saved_model.load('saved')

# Set the path for recording
audio_path = "data/output.wav"

# A function for recording a 1 second clip of audio
def Record():
    seconds = 1
    sampleRate = 44100
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

    print("Successfully Recorded.")
    return None


# A function to pass audio into the model
# returns 
# def use_model(audio_path):
    # model out contains all information gathered from using the model -> the in/out tensors, the prediction values, the prediction with the highest value, etc.
#    model_out = sherpa_asr(tf.constant(str(audio_path)))

    # this grabs the prediction values from the output of the model, has form: [[ 0.20681217  0.4543526  -0.65284234  0.07148097 -0.3101785  -0.51415586 -0.23595797 -0.64456975]]
#    predictions_arr = model_out['predictions'].numpy()   
#    print("predictions_arr: ")
#    print(predictions_arr)

    # this grabs the highest prediction value from the output of the model, has form: [b'go']    
#    highPred = np.array2string(predictions_arr['class_names'].numpy())
#    print("highPred: ")
#    print(highPred)

#    return predictions_arr, model_out

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

exitCheck = 0
while (exitCheck == 0):
    print("Would you like to run a command?")
    userChoice = input("Enter yes or no: ")
    if (userChoice == "yes"):
        
        Record()

        run_up, out = use_model(audio_path)
        print("out[3]: ", out[3])

        count, ans = veri_n_ind(out)
        print("count: ", count)
        print("ans: ", ans)

        ans = keywords[count]
        print("ans: ", ans)

        commandExec(ans)

    elif (userChoice == "no"):
        print("Exiting.")
        exitCheck = 1