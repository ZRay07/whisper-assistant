from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import numpy as np
import soundfile as sf
import sounddevice as sd
import wavio as wv

# Set the path for recording
RECORD_PATH = "data/output.wav"


class Recorder:
    def __init__(self):
        self.record_frequency = 16000

    def record(self, record_duration):
        try:
            print("\nListening...")

            # Start recorder with the given values
            self.recording = sd.rec(
                int(record_duration * self.record_frequency),
                samplerate=self.record_frequency,
                channels=1,
                dtype=np.float64,
            )

            # Record audio for the given number of seconds
            sd.wait()

            # Convert the NumPy array to audio file
            wv.write(RECORD_PATH, self.recording, self.record_frequency, samp_width=1)

            return True

        except Exception as e:
            print(f"Error occured during transcription: {e}")
            return False


class ASR_Model:
    def __init__(self):
        try:
            # Load the ASR processor and model from pre-trained checkpoints
            self.processor = AutoProcessor.from_pretrained("openai/whisper-tiny.en")
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
                "openai/whisper-tiny.en"
            )
            print("Model & processor loaded successfully")

        except Exception as e:
            print(f"Error occured during processor/model loading: {e}")

    def use_model(self, path_to_audio, real_time=False):
        try:
            # Read audio data from the specified path
            self.data, self.srate = sf.read(path_to_audio)

            if not real_time:
                print("Processing...")

            # Preprocess the audio data using the processor
            self.input_features = self.processor(
                self.data, sampling_rate=16000, return_tensors="pt"
            ).input_features

            # Generate the transcription using the ASR model
            self.predicted_ids = self.model.generate(
                self.input_features, max_length=448
            )

            # Decode the predicted IDs into text using the processor
            self.transcription = self.processor.batch_decode(
                self.predicted_ids, skip_special_tokens=True
            )

            # Format the transcription result
            self.formatted_transcription = self.transcription[0]
            self.formatted_transcription = self.formatted_transcription[1:]
            return self.formatted_transcription

        except Exception as e:
            print(f"Error occured during transcription: {e}")
            return False


# Create instances of Recorder and ASR_model
microphone = Recorder()
whisper = ASR_Model()
