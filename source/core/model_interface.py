from transformers import AutoModelForSpeechSeq2Seq,  AutoProcessor
import numpy as np
import soundfile as sf
import sounddevice as sd
import wavio as wv

# Set the path for recording
RECORD_PATH = "data/output.wav"

class Recorder:
    def __init__(self):
        self.recordFrequency = 16000

    def record(self, recordDuration):
        try:
            print("\nListening...")
    
            # Start recorder with the given values
            self.recording = sd.rec(int(recordDuration * self.recordFrequency),
                                    samplerate = self.recordFrequency, channels = 1, dtype = np.float64)
    
            # Record audio for the given number of seconds
            sd.wait()
    
            # Convert the NumPy array to audio file
            wv.write(RECORD_PATH, self.recording, self.recordFrequency, sampwidth = 1)

            return True
        
        except Exception as e:
            print(f"Error occured during transcription: {e}")
            return False


class ASR_model:
    def __init__(self):
        try:
             # Load the ASR processor and model from pre-trained checkpoints
            self.processor = AutoProcessor.from_pretrained("openai/whisper-tiny.en")
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-tiny.en")
            print("Model & processor loaded successfully")
        
        except Exception as e:
            print(f"Error occured during processor/model loading: {e}")
        
    def use_model(self, pathToAudio):
        try:
            # Read audio data from the specified path
            self.data, self.srate = sf.read(pathToAudio)

            print("Processing...")

            # Preprocess the audio data using the processor
            self.input_features = self.processor(self.data, sampling_rate = 16000, return_tensors ="pt").input_features

            # Generate the transcription using the ASR model
            self.predicted_ids = self.model.generate(self.input_features, max_length = 448)

            # Decode the predicted IDs into text using the processor
            self.transcription = self.processor.batch_decode(self.predicted_ids, skip_special_tokens=True)

            # Format the transcription result
            self.formattedTranscription = self.transcription[0]
            self.formattedTranscription = self.formattedTranscription[1:]
            return self.formattedTranscription
        
        except Exception as e:
            print(f"Error occured during transcription: {e}")
            return False


if __name__ == "__main__":
    # Create instances of Recorder and ASR_model
    microphone = Recorder()
    whisper = ASR_model()

