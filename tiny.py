
from transformers import WhisperProcessor, WhisperForConditionalGeneration, AutoModelForSpeechSeq2Seq,  AutoProcessor
import numpy as np
import soundfile as sf
from datasets import load_dataset
data, srate =sf.read("C:/Users/cohent1/Documents/Senior_yr/Senior_Design/using_model/Senior_Design-main/Senior_Design-main/data/mini_speech_commands/down/00b01445_nohash_1.wav")
def use_model(data):
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