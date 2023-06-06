
from transformers import WhisperProcessor, WhisperForConditionalGeneration, AutoModelForSpeechSeq2Seq,  AutoProcessor
import numpy as np
import soundfile as sf
from datasets import load_dataset
data, srate =sf.read("C:/Users/cohent1/Documents/Senior_yr/174-168635-0000.wav")
def use_model(data):
    processor = AutoProcessor.from_pretrained("openai/whisper-medium")
    model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-medium")
#sample = ds["audio"]
#audio = np.load(audio_path, allow_pickle = True)
    input_features = processor(data, sampling_rate = 16000, return_tensors ="pt").input_features
    predicted_ids = model.generate(input_features, max_length = 448)
    transcription = processor.batch_decode(predicted_ids,skip_special_tokens=True)
    return transcription

best_guess = use_model(data)
print(best_guess)