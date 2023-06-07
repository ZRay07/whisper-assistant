from transformers import WhisperProcessor, WhisperForConditionalGeneration, AutoModelForSpeechSeq2Seq,  AutoProcessor
import numpy as np
import soundfile as sf
from datasets import load_dataset

import sounddevice as sd
from scipy.io import wavfile
import wavio as wv
from playsound import playsound

from source.core.command_module import commandExec

# Set the path for recording
RECORD_PATH = "data/output.wav"

class Recorder:

    def __init__(self):
        self.recordFrequency = 44100
        self.recordDuration = 5

    def record(self):
        
        print(sd.query_devices())
        
        print("Listening...")
        # Sampling frequency
        self.freq = 44100
 
        # Recording duration
        self.duration = 5
 
        # Start recorder with the given values
        # of duration and sample frequency
        self.recording = sd.rec(int(self.duration * self.freq),
                   samplerate=self.freq, channels=1) #, dtype = np.float64)
 
        # Record audio for the given number of seconds
        sd.wait()
 
        # This will convert the NumPy array to an audio
        # file with the given sampling frequency
        wavfile.write("data/recording.wav", self.freq, self.recording)
 
        # Convert the NumPy array to audio file
        wv.write("data/recording1.wav", self.recording, self.freq, sampwidth=2)

        self.data, self.srate = sf.read("data/recording1.wav")

data, srate =sf.read("data/mini_speech_commands/down/00b01445_nohash_1.wav")
def use_model(data):
    print("Processing...")
    processor = AutoProcessor.from_pretrained("openai/whisper-tiny.en")
    model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-tiny.en")
#sample = ds["audio"]
#audio = np.load(audio_path, allow_pickle = True)
    input_features = processor(data, sampling_rate = 16000, return_tensors ="pt").input_features
    predicted_ids = model.generate(input_features, max_length = 448)
    transcription = processor.batch_decode(predicted_ids,skip_special_tokens=True)
    return transcription

best_guess = use_model(data)
print(best_guess)

recordClass = Recorder()

recordClass.record()

result = use_model(recordClass.data)
print(result)

