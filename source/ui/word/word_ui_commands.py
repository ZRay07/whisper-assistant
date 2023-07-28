import io
import os
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

from source.core.model_interface import whisper

import speech_recognition as sr
import pyautogui
    # Ctrl+End is a keyboard shortcut that moves the cursor to the end of a document.
class WordCommandHandler():

    def save_file(self):
        print("save file")

    def tab_text(self):
        print("tab text")
        
    def new_line(self):
        print("new line")
        
    def new_page(self):
        print("new page")

    def increase_font_size(self):
        print("increase font size")

    def decrease_font_size(self):
        print("decrease font size")



    def real_time_text_input(): # from https://github.com/davabase/whisper_real_time
        audio_model = whisper

        # Energy level for mic to detect
        energy_threshold = 1000

        # How real time the recording is in seconds
        record_timeout = 2

        # How much empty space between recordings before we consider it a new line in the transcription
        phrase_timeout = 3

        temp_file = NamedTemporaryFile().name
        transcription = ['']
        previous_transcription = ['']
        transcription_changed = False

        # The last time a recording was retreived from the queue.
        phrase_time = None
        # Current raw audio bytes.
        last_sample = bytes()
        # Thread safe Queue for passing data from the threaded recording callback.
        data_queue = Queue()

        # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
        recorder = sr.Recognizer()
        recorder.energy_threshold = energy_threshold
        # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
        recorder.dynamic_energy_threshold = False

        source = sr.Microphone(sample_rate=16000)
        with source:
            recorder.adjust_for_ambient_noise(source)

        def record_callback(_, audio:sr.AudioData) -> None:
            """
            Threaded callback function to recieve audio data when recordings finish.
            audio: An AudioData containing the recorded bytes.
            """
            # Grab the raw bytes and push it into the thread safe queue.
            data = audio.get_raw_data()
            data_queue.put(data)

        # Create a background thread that will pass us raw audio bytes.
        # We could do this manually but SpeechRecognizer provides a nice helper.
        recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

        # Cue the user that we're ready to go.
        print("Model loaded.\n")

        while True:
            try:
                now = datetime.utcnow()
                # Pull raw recorded audio from the queue.
                if not data_queue.empty():
                    phrase_complete = False
                    # If enough time has passed between recordings, consider the phrase complete.
                    # Clear the current working audio buffer to start over with the new data.
                    if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                        last_sample = bytes()
                        phrase_complete = True
                    # This is the last time we received new audio data from the queue.
                    phrase_time = now

                    # Concatenate our current audio data with the latest audio data.
                    while not data_queue.empty():
                        data = data_queue.get()
                        last_sample += data

                    # Use AudioData to convert the raw data to wav data.
                    audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                    wav_data = io.BytesIO(audio_data.get_wav_data())

                    # Write wav data to the temporary file as bytes.
                    with open(temp_file, 'w+b') as f:
                        f.write(wav_data.read())

                    # Read the transcription.
                    result = audio_model.use_model(temp_file, True)
                    text = result

                    # If we detect exit as the last word, exit the loop
                    exit_keywords = {"Exit.", " Exit", " exit"}
                    print(f"text[-1]: {text[-5:]}")
                    if text[-5:] in exit_keywords:
                        break

                    # If we detected a pause between recordings, add a new item to our transcripion.
                    # Otherwise edit the existing one.
                    if phrase_complete:
                        transcription.append(text)
                        
                    else:
                        transcription[-1] = text

                    # Check if transcription has changed
                    if transcription != previous_transcription:
                        transcription_changed = True
                        previous_transcription = transcription.copy()
                    else:
                        transcription_changed = False

                    if transcription_changed:
                        numberOfBackSpaces = []     # This nifty little bit of code: https://www.reddit.com/r/learnpython/comments/117j3ou/question_with_pyautogui_delete_text_and_replace/
                        for line in transcription:
                            for char in range(0, len(line) + 1): 
                                numberOfBackSpaces.append('backspace')
                        
                        pyautogui.press(numberOfBackSpaces)

                        for line in transcription:
                            pyautogui.write(line)


                    # Clear the console to reprint the updated transcription.
                    os.system('cls')
                    for line in transcription:
                        print(line)

                    # Flush stdout.
                    print('', end='', flush=True)
                    

                    # Infinite loops are bad for processors, must sleep.
                    sleep(0.25)
            except KeyboardInterrupt:
                break

        print("\n\nTranscription:")
        for line in transcription:
            print(line)
            #pyautogui.write(line)

if __name__ == "__main__":
    command_handler = WordCommandHandler()
    command_handler.real_time_text_input()