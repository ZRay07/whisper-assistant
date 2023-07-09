import unittest
import json
import os
from source.core.command_module import handleApplicationAction
from source.core.command_module import handleScrollAction
from source.core.command_module import setVolume
from source.core.command_module import loadValidApps
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
        self.assertTrue(handleScrollAction("up", "up"),
                        "Expected scroll up by 100 'clicks'")
        
    def test_scrollUp(self):
        self.assertTrue(handleScrollAction("10", "up"),
                        "Expected scroll up by 10 'clicks'")
        
    def test_scrollUpWord(self):
        self.assertTrue(handleScrollAction("Ten", "up"),
                        "Expected scroll up by 10 'clicks'")
        
    def test_falseScrollUp(self):
        self.assertFalse(handleScrollAction("A","up"),
                         "Expected failed scrolling up")
        
    def test_scrollDownDefault(self):
        self.assertTrue(handleScrollAction("down", "down"),
                        "Expected scroll down by 100 'clicks'")
        
    def test_scrollDown(self):
        self.assertTrue(handleScrollAction("10", "down"),
                        "Expected scroll down by 10 'clicks'")
        
    def test_scrollDownword(self):
        self.assertTrue(handleScrollAction("Ten", "down"),
                        "Expected scroll down by 10 'clicks'")
        
    def test_falseScrollDown(self):
        self.assertFalse(handleScrollAction("A", "down"),
                         "Expected failed scrolling down")
        
#class testSetVolumeMethods(unittest.TestCase):
#    def test_setVolumeTo0(self):
#        self.assertEqual(0, setVolume("0"), 
#                         "Expected volume to be set to 0.")

if __name__ == '__main__':
    unittest.main()