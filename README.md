<h2 align="center">Hi 👋, we're Tyler Cohen, Devin Chen, and Zach Ray</h2>
<h3 align="center">A group of seniors at Wentworth Institute of Technology</h3>

<h1 align="center">We're currently working on [S.H.E.R.P.A.]</h1>

Our *Super Helpful Engine Recognizing People's Audio* uses OpenAI's Whisper to translate speech into text. After we convert speech to text,
we pass our user's request to the command module. The command module runs a command based on the users request.
The goal is to build commands so that a user can control their computer through voice.
Basically, a recreation of Cortana or Siri.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for use and testing purposes.

## Installation
* Download the code and unzip it.  
* Save the file directory.  
* Open command prompt by typing 'cmd' in Windows search bar

### Create a virtual environment
* This stores all of the required packages inside of a folder and keeps them seperate from the global Python installation. 
* You can create an environment with
```
python -m venv C:\path\to\project\dir\venv
```

* Now you want to activate the environment.  
* Navigate to the directory where the code is unzipped.
* Enter the virtual environment directory
* Enter the Scripts folder of the virtual environment.
```
cd C:\path\to\project\dir
cd venv
cd Scripts
```
* Ensure you are in the Scripts folder of your virtual environment. 
* Activate the environment with: `activate`

If you've activated the environment successfully, you should see a __*(venv)*__ in the command prompt now preceding the line.

### Install required packages
Ensure you are in your project's directory.
Now that you have your virtual environment activated, install the required packages with: 
```
pip install -r requirements.txt
```
You should be able to run the program now.

## Tutorial / User Manual
* Navigate to the dir where the project exists
* Run the program with: 
```
python -m source.ui.ui
```

You should see this window, built with Tkinter.

![alt text](https://github.com/TationtoC/Senior_Design/blob/test_branch/readME/sherpaMainWindow.PNG "SHERPA Main Window")

* In the left frame, you will see there is a list of commands.
    1. Open / Close Application
    1. Scroll Up / Down
    1. Set Volume
    1. Navigate Mouse and Keyboard
    1. Email sign-in

* In the right frame
    1. A button to initiate microphone recording.
        * The recording duration lasts **3** seconds.
        * The label below the record button displays the command which the model heard.
    1. An additional button to record a transcription.
        * This recording duration lasts **15** seconds.
        * The box above the transcription button displays the transcription which the model heard.

#### Example use case
* To open an application on your computer
    1. Hit the record button
    1. Say "Open application" or "open app"
    1. You should be prompted to say the name of the application you wish to open
        * For example, you can say "Spotify" or "Word"
    1. The AppOpener package searches your PC for a matching application and launches it!

Note: Some commands are end to end and require no additional information from the user. If the command requires additional information, such as
an application name - you will be prompted.

## Running the tests
TO-DO: Create test audio files so we can show the model in action.

TO-DO: Create test functions to run commands and ensure correct output.

## Built With
* [Whisper](https://platform.openai.com/docs/introduction) - The speech recognition model used.
* [Tkinter](https://docs.python.org/3/library/tkinter.html#) - From Python's standard library.
* And a multitude of packages used in command creation. Check requirements.txt for specific package list.

## Acknowledgements
* Special thanks to Tyler's friend for early help on ML models.
* Inspiration: Creating accessibility software so access to computers is available to everyone. Including grandparents (who may not be as technologically proficient).