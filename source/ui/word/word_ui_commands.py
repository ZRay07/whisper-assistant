import io
import os
from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

from source.core.model_interface import whisper
from source.ui.mouse_grid.mouse_grid_input import MouseGridInputValidator

import speech_recognition as sr
import pyautogui

class WordCommandHandler():
    def __init__(self, ui, input_window = None):
        self.word_ui = ui
        self.input_window = input_window

        self.ribbon_popup_delay = 0.85
        self.sequential_key_delay = 0.2
        self.hotkey_delay = 0.25

        self.initial_save = False

        self.x_center_screen = self.word_ui.winfo_screenwidth() / 2
        self.y_center_screen = self.word_ui.winfo_screenheight() / 2

    def window_back_and_forth(word_command):
        # This is a decorator function
        # A decorator function essentially performs the same preprocessing and postprocessing steps
        #       to a function that uses the decorator
        # for more information: https://www.geeksforgeeks.org/decorators-in-python/
        def wrapper(*args, **kwargs):
            self = args[0]

            # Push the UI window back
            #self.word_ui.lower()
        
            # Click on the Word window
            #pyautogui.doubleClick(self.x_center_screen, self.y_center_screen)

            pyautogui.hotkey("alt", "tab")

            result = word_command(*args, **kwargs)

            # Lift the UI window upfront
            #self.word_ui.focus_force()

            pyautogui.hotkey("alt", "tab")

            return result
        
        return wrapper
    
    @window_back_and_forth
    def insert_text(self, textInput):
        print("text insert")

        # First, move to the end of the docoment
        pyautogui.hotkey("ctrl", "end")
        sleep(self.hotkey_delay)

        for line in textInput:
            pyautogui.write(line, interval = 0.1)

        return f"Successfully typed: {textInput}"
    
    def insert_transcript(self, textInput):
        print("text insert")

        # First, move to the end of the docoment
        pyautogui.hotkey("ctrl", "end")
        sleep(self.hotkey_delay)

        pyautogui.write(textInput, interval = 0.1)
        return f"Successfully typed: {textInput}"

    @window_back_and_forth
    def save_file(self):
        print("save file")

        if self.initial_save:
            # Use control s to save document
            pyautogui.hotkey("ctrl", "s")

        else:
            self.word_ui.setLabel(self.word_ui.feedback_msg.error_label2, "You must perform 'save file as' first")

    @window_back_and_forth
    def save_and_name_file(self):
        print("save file as")
        file_name = self.word_ui.document_name
        key_stream = ["f", "a", "c", "y", "3"]

        # Alt brings up the ribbon keys
        pyautogui.press("alt")

        # A small delay allows the ribbon options to pop up
        sleep(self.ribbon_popup_delay)

        # Go through the hotkeys until we reach file name location
        for key in key_stream:
            pyautogui.press(key)
            sleep(self.sequential_key_delay)

        # Type in the file name
        pyautogui.typewrite(file_name, interval = 0.1)

        # Tab over to save button
        pyautogui.press("tab", presses = 2)

        # Press the save button
        pyautogui.press("enter")

        self.initial_save = True

    @window_back_and_forth
    def tab_text(self):
        print("tab text")
        pyautogui.press("tab")

    @window_back_and_forth 
    def new_line(self):
        print("new line")
        pyautogui.hotkey("enter")
        
    @window_back_and_forth
    def new_page(self):
        print("new page")
        pyautogui.hotkey("ctrl", "enter")

    @window_back_and_forth
    def change_font(self, font):
        print("change font")
        key_stream = ["down", "right", "right"]

        pyautogui.press("alt")
        sleep(self.ribbon_popup_delay)

        for key in key_stream:
            pyautogui.press(key)
            sleep(self.sequential_key_delay)

        pyautogui.typewrite(font)

    @window_back_and_forth
    def increase_font_size(self):
        print("increase font size")
        pyautogui.hotkey("ctrl", "]")

    @window_back_and_forth
    def decrease_font_size(self):
        print("decrease font size")
        pyautogui.hotkey("ctrl", "[")

    @window_back_and_forth
    def make_font_bold(self):
        print("make font bold")
        pyautogui.hotkey("ctrl", "b")

    @window_back_and_forth
    def make_font_italic(self):
        print("make font bold")
        pyautogui.hotkey("ctrl", "i")

    @window_back_and_forth
    def make_font_underline(self):
        print("make font bold")
        pyautogui.hotkey("ctrl", "u")

    @window_back_and_forth
    def make_title_style(self):
        print("title style")

    @window_back_and_forth
    def make_heading1_style(self):
        print("heading 1")

    @window_back_and_forth
    def make_heading2_style(self):
        print("heading 2")

    @window_back_and_forth
    def make_normal_style(self):
        print("normal")

    @window_back_and_forth
    def make_subscript(self):
        print("subscript")
        pyautogui.hotkey("ctrl", "=")

    @window_back_and_forth
    def make_superscript(self):
        print("superscript")
        pyautogui.hotkey("ctrl", "shift", "+")

    @window_back_and_forth
    def delete_word(self, textInput):
        print("word delete")

        # First, move to the end of the docoment
        pyautogui.hotkey("ctrl", "h")
        sleep(self.hotkey_delay)

        pyautogui.write(textInput, interval = 0.1)

        sleep(self.sequential_key_delay)

        pyautogui.press("enter")

        pyautogui.hotkey("shift", "tab")
        
        sleep(self.sequential_key_delay)

        pyautogui.hotkey("shift", "tab")

        sleep(self.sequential_key_delay)

        pyautogui.press("enter")

        sleep(self.sequential_key_delay)

        pyautogui.press("tab")

        sleep(self.sequential_key_delay)

        pyautogui.press("tab")

        sleep(self.sequential_key_delay)

        pyautogui.press("enter")

        return f"Successfully deleted: {textInput}"

    @window_back_and_forth
    def mouse_control(self):
        print("mouse control")
        self.mouseGrid = MouseGridInputValidator()
            
        # Bring back the main screen window
        if self.mouseGrid.typeSomething:    # If we type something, we wanna wait for longer
            sleep(self.mouseGrid.recordDuration / 10)
        else:
            sleep(1)

    
    def real_time_text_input(self): # from https://github.com/davabase/whisper_real_time
        pyautogui.click(self.x_center_screen, self.y_center_screen)
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
                    exit_keywords = {"Exit.", " Exit", " exit", "exit.", "exit"}
                    print(f"text[-5:]: {text[-5:]}")
                    if text[-5:] in exit_keywords:
                        break
                    elif text[-4:] in exit_keywords:
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

                    #if transcription_changed:
                        #numberOfBackSpaces = 0     # This nifty little bit of code: https://www.reddit.com/r/learnpython/comments/117j3ou/question_with_pyautogui_delete_text_and_replace/
                        #print(f"number_of_back_spaces: {numberOfBackSpaces}")
                        #for line in transcription:
                            #for char in range(0, len(line)):
                                #print(f"number_of_back_spaces: {numberOfBackSpaces}")
                                #numberOfBackSpaces += 1;
                        
                        #pyautogui.press("backspace", presses = numberOfBackSpaces)

                        #for line in transcription:
                            #pyautogui.write(line)

                    if transcription_changed:
                        input_text = " ".join(transcription)
                        self.word_ui.setLabel(self.word_ui.text_input.user_text, input_text)


                    # Clear the console to reprint the updated transcription.
                    #os.system('cls')
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

        return transcription

if __name__ == "__main__":
    command_handler = WordCommandHandler()
    command_handler.real_time_text_input()