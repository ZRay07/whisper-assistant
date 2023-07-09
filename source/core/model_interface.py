from transformers import WhisperProcessor, WhisperForConditionalGeneration, AutoModelForSpeechSeq2Seq,  AutoProcessor
import numpy as np
import soundfile as sf
from datasets import load_dataset

import sounddevice as sd
from scipy.io import wavfile
import wavio as wv

# Set the path for recording
RECORD_PATH = "data/output.wav"

class Recorder:

    def __init__(self):
        self.recordFrequency = 16000

    def record(self, recordDuration):
        print("\nListening...")
 
        # Start recorder with the given values
        self.recording = sd.rec(int(recordDuration * self.recordFrequency),
                                samplerate = self.recordFrequency, channels = 1, dtype = np.float64)
 
        # Record audio for the given number of seconds
        sd.wait()
 
        # Convert the NumPy array to audio file
        wv.write(RECORD_PATH, self.recording, self.recordFrequency, sampwidth = 1)

class ASR_model:
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("openai/whisper-tiny.en")
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-tiny.en")
        
    def use_model(self, pathToAudio):

        self.data, self.srate = sf.read(pathToAudio)

        print("Processing...")
#sample = ds["audio"]
#audio = np.load(audio_path, allow_pickle = True)
        self.input_features = self.processor(self.data, sampling_rate = 16000, return_tensors ="pt").input_features
        self.predicted_ids = self.model.generate(self.input_features, max_length = 448)
        self.transcription = self.processor.batch_decode(self.predicted_ids, skip_special_tokens=True)

        self.formattedTranscription = self.transcription[0]
        self.formattedTranscription = self.formattedTranscription[1:]
        return self.formattedTranscription


microphone = Recorder()
whisper = ASR_model()

if __name__ == "__main__":
    print("This should only run if called from cmd line")

