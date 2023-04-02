# SHERPA
**Speech -> Text -> Command**

## Installation
Download the code and unzip it.
Save the file directory.
Open command prompt by typing 'cmd' in Windows search bar

You're going to want to create a virtual environment
This stores all of the required packages inside of a folder and keeps them seperate
from the global Python installation
You can create an environment with
> python -m venv C:\path\to\project\dir\.venv

Now you want to activate the environment
Navigate to the directory where the code is unzipped
> cd C:\path\to\project\dir

Activate the environment with:
> C:\path\to\project\dir\.venv\Scripts\activate.bat

You should see a (venv) in the command prompt now preceding the line

Now that you have your virtual environment activated, install the required packages with:
> pip install -r requirements.txt

## Tutorial
Navigate to the dir where the project exists
Run a specific module with:
> python -m folder1.folder2.example_module
such as:
> python -m source.core.asr_module
which runs the model training