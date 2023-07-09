import unittest
import json
import os
from source.core.command_module import handleApplicationAction
from source.core.command_module import handleScrollAction
from source.core.command_module import setVolume
from source.core.command_module import loadValidApps
from source.core.command_module import convertToInt, convertWordToInt
class testApplicationMethods(unittest.TestCase):

    def test_loadValidApps(self):
        # Create a mock JSON file with some app names
        app_data = {
            "Word": "C:/Program Files/Microsoft Office/Word.exe",
            "Excel": "C:/Program Files/Microsoft Office/Excel.exe",
            "PowerPoint": "C:/Program Files/Microsoft Office/PowerPoint.exe",
            "Chrome": "C:/Program Files/Google/Chrome.exe"
        }

        # Save the mock data to a JSON file
        with open("data/app_data.json", "w") as json_file:
            json.dump(app_data, json_file)

        # Call the function being tested
        validApps = loadValidApps()

        # Check the expected output
        expectedApps = set(app_data.keys())
        self.assertEqual(validApps, expectedApps, "Loaded valid apps do not match the expected apps")

        # Clean up the mock JSON file
        os.remove("data/app_data.json")
    
    def test_handleApplicationAction_open(self):
        app_data = {"spotify": "SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"}

        # Save the spotify data to a JSON file
        with open("data/app_data.json", "w") as json_file:
            json.dump(app_data, json_file)

        appName = "spotify"
        action = "open"
        expectedOutput = True

        result = handleApplicationAction(appName, action)
        self.assertEqual(result, expectedOutput, f"Failed to open application: {appName}")

        # Clean up the mock JSON file
        os.remove("data/app_data.json")

    def test_handleApplicationAction_close(self):
        app_data = {"spotify": "SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify"}

        # Save the spotify data to a JSON file
        with open("data/app_data.json", "w") as json_file:
            json.dump(app_data, json_file)

        appName = "spotify"
        action = "close"
        expectedOutput = True

        result = handleApplicationAction(appName, action)
        self.assertEqual(result, expectedOutput, f"Failed to close application: {appName}")

        # Clean up the mock JSON file
        os.remove("data/app_data.json")
        
    def test_handleApplicationAction_invalidAppName(self):
        appName = "INVALID_APPNAME"
        action = "open"
        expectedOutput = False

        result = handleApplicationAction(appName, action)
        self.assertEqual(result, expectedOutput, f"Invalid application name: {appName}")

    def test_handleApplicationAction_invalidAction(self):
        appName = "spotify"
        action = "INVALID_ACTION"
        expectedOutput = False

        result = handleApplicationAction(appName, action)
        self.assertEqual(result, expectedOutput, f"Invalid action: {action}")
        
class testScrollMethods(unittest.TestCase):

    def test_scrollUpDefault(self):
        scrollAmount = "up"
        direction = "up"
        expectedOutput = True

        result = handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, "Expected scroll up by 100 'clicks'")
        
    def test_scrollUp(self):
        scrollAmount = "10"  # Simulated scroll amount
        direction = "up"
        expectedOutput = True

        result = handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, "Expected scroll up by 10 'clicks'")
        
    def test_scrollUpWord(self):
        scrollAmount = "ten"  # Simulated scroll amount
        direction = "up"
        expectedOutput = True

        result = handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, "Expected scroll up by 10 'clicks'")
        
    def test_scrollDownDefault(self):
        scrollAmount = "down"
        direction = "down"
        expectedOutput = True

        result = handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, "Expected scroll down by 100 'clicks'")
        
    def test_scrollDown(self):
        scrollAmount = "10"  # Simulated scroll amount
        direction = "down"
        expectedOutput = True

        result = handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, "Expected scroll down by 10 'clicks'")
        
    def test_scrollDownWord(self):
        scrollAmount = "ten"  # Simulated scroll amount
        direction = "down"
        expectedOutput = True

        result = handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, "Expected scroll down by 10 'clicks'")

class TestConversionMethods(unittest.TestCase):

    def test_convertToInt_ValidInput(self):
        # Test with valid integer input
        stringValue = "42"
        expectedOutput = 42

        result = convertToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to match the input integer value")

    def test_convertToInt_InvalidInput(self):
        # Test with invalid input (non-numeric string)
        stringValue = "abc"
        expectedOutput = None

        result = convertToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to be None for invalid input")

    def test_convertWordToInt_IntegerInput(self):
        # Test with integer input
        stringValue = 42
        expectedOutput = 42

        result = convertWordToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to match the input integer value")

    def test_convertWordToInt_StringInput(self):
        # Test with string input representing a number
        stringValue = "Ten"
        expectedOutput = 10

        result = convertWordToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to be the numeric representation of the word")

    def test_convertWordToInt_InvalidInput(self):
        # Test with invalid input (neither integer nor string)
        stringValue = 3.14
        expectedOutput = None

        result = convertWordToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to be None for invalid input")

    def test_convertWordToInt_InvalidWord(self):
        # Test with an invalid word that cannot be converted to a number
        stringValue = "Invalid"
        expectedOutput = None

        result = convertWordToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to be None for an invalid word")

#class testSetVolumeMethods(unittest.TestCase):
#    def test_setVolumeTo0(self):
#        self.assertEqual(0, setVolume("0"), 
#                         "Expected volume to be set to 0.")

if __name__ == '__main__':
    unittest.main()