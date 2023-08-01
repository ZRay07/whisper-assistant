import unittest
from unittest.mock import patch
import json
import os
from source.core.command_module import operations
from source.core.command_module import loadValidApps


class testOpenApplicationMethods(unittest.TestCase):
    def setUp(self):
        self.Commands = operations()
        self.TEST_APPS = ["word", "excel", "powerpoint", "chrome"]

    def tearDown(self):
        pass

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

        # Explicitly close the file
        json_file.close()

        # Call the function being tested
        validApps = loadValidApps()

        # Check the expected output
        expectedApps = set(app_data.keys())
        self.assertEqual(validApps, expectedApps, "Loaded valid apps do not match the expected apps")

        # Clean up the mock JSON file
        os.remove("data/app_data.json")
    
    @patch("source.core.command_module.app_opener_open")
    def test_handleApplicationAction_OpenValid(self, mock_app_opener_open):
        appName = "word"
        action = "open"

        mock_app_opener_open.return_value = None

        expectedOutput = "open word successful."
        errorMessage = "Open application with valid app and valid action does not match expected output"

        result = self.Commands.handleApplicationAction(appName, action, self.TEST_APPS)
        self.assertEqual(result, expectedOutput, errorMessage)

    @patch("source.core.command_module.app_opener_open")
    def test_handleApplicationAction_OpenInvalidAppName(self, mock_app_opener_open):
        appName = "INVALID_APPNAME"
        action = "open"

        mock_app_opener_open.return_value = None
        expectedOutput = "open INVALID_APPNAME NOT successful."
        errorMessage = "Open application with invalid app and valid action does not match expected output"

        result = self.Commands.handleApplicationAction(appName, action, self.TEST_APPS)
        self.assertEqual(result, expectedOutput, errorMessage)

    @patch("source.core.command_module.app_opener_open")
    def test_handleApplicationAction_OpenInvalidAction(self, mock_app_opener_open):
        appName = "word"
        action = "INVALID_ACTION"

        mock_app_opener_open.return_value = None

        expectedOutput = "INVALID_ACTION word NOT successful."
        errorMessage = "Open application with valid app and invalid action does not match expected output"

        result = self.Commands.handleApplicationAction(appName, action, self.TEST_APPS)
        self.assertEqual(result, expectedOutput, errorMessage)

    @patch("source.core.command_module.app_opener_open")
    def test_handleApplicationAction_InvalidActionInvalidAppName(self, mock_app_opener_open):
        appName = "INVALID_APPNAME"
        action = "INVALID_ACTION"

        mock_app_opener_open.return_value = None

        expectedOutput = "INVALID_ACTION INVALID_APPNAME NOT successful."
        errorMessage = "Open application with valid app and invalid action does not match expected output"

        result = self.Commands.handleApplicationAction(appName, action, self.TEST_APPS)
        self.assertEqual(result, expectedOutput, errorMessage)

class testCloseApplicationMethods(unittest.TestCase):
    def setUp(self):
        self.Commands = operations()
        self.TEST_APPS = ["word", "excel", "powerpoint", "chrome"]

    @patch("source.core.command_module.app_opener_close")
    def test_handleApplicationAction_CloseValid(self, mock_app_opener_close):
        appName = "word"
        action = "close"

        mock_app_opener_close.return_value = None

        expectedOutput = "close word successful."
        errorMessage = "Close application with valid app and valid action does not match expected output"

        result = self.Commands.handleApplicationAction(appName, action, self.TEST_APPS)
        self.assertEqual(result, expectedOutput, errorMessage)

    @patch("source.core.command_module.app_opener_close")
    def test_handleApplicationAction_CloseInvalidAppName(self, mock_app_opener_close):
        appName = "INVALID_APPNAME"
        action = "close"

        mock_app_opener_close.return_value = None

        expectedOutput = "close INVALID_APPNAME NOT successful."
        errorMessage = "Close application with invalid app and valid action does not match expected output"

        result = self.Commands.handleApplicationAction(appName, action, self.TEST_APPS)
        self.assertEqual(result, expectedOutput, errorMessage)

    def test_test_handleApplicationAction_CloseNonOpenApp(self):
        appName = "word"
        action = "close"

        expectedOutput = "An exception occured while closeing word"
        errorMessage = "Close application with invalid app and valid action does not match expected output"

        result = self.Commands.handleApplicationAction(appName, action, self.TEST_APPS)
        self.assertEqual(result, expectedOutput, errorMessage)

class testScrollMethods(unittest.TestCase):
    def setUp(self):
        self.Commands = operations()

    def test_scrollUpDefault(self):
        scrollAmount = 100
        direction = "up"
        expectedOutput = "Scrolled up by 100 click(s)"
        errorMessage = "Default scroll up amount does not match expected output"

        result = self.Commands.handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, errorMessage)
        
    def test_scrollUp(self):
        scrollAmount = 10  # Simulated scroll amount
        direction = "up"
        expectedOutput = "Scrolled up by 10 click(s)"
        errorMessage = "Scroll up amount does not match expected output"

        result = self.Commands.handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, errorMessage)
        
    def test_scrollDownDefault(self):
        scrollAmount = 100
        direction = "down"
        expectedOutput = "Scrolled down by 100 click(s)"
        errorMessage = "Scroll amount does not match expected output"

        result = self.Commands.handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, errorMessage)
        
    def test_scrollDown(self):
        scrollAmount = 10  # Simulated scroll amount
        direction = "down"
        expectedOutput = "Scrolled down by 10 click(s)"
        errorMessage = "Scroll amount does not match expected output"

        result = self.Commands.handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, expectedOutput, errorMessage)
        
    def test_scrollInvalidDirection(self):
        scrollAmount = 500  # Simulated scroll amount
        direction = "INVALID_DIRECTION"
        errorMessage = "Invalid scroll direction does not match expected output"

        result = self.Commands.handleScrollAction(scrollAmount, direction)
        
        self.assertEqual(result, 'Invalid scroll direction: INVALID_DIRECTION', errorMessage)

    def test_scrollInvalidScrollAmount(self):
        scrollAmount = "INVALID_SCROLL_AMOUNT"  # Simulated scroll amount
        direction = "up"
        errorMessage = "Invalid scroll amount does not match expected output"
        
        result = self.Commands.handleScrollAction(scrollAmount, direction)
        self.assertEqual(result, "Invalid scroll amount: INVALID_SCROLL_AMOUNT", errorMessage)

class TestConversionMethods(unittest.TestCase):
    def setUp(self):
        self.Commands = operations()

    def test_convertToInt_ValidInput(self):
        # Test with valid integer input
        stringValue = "42"
        expectedOutput = 42

        result = self.Commands.convertToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to match the input integer value")

    def test_convertToInt_ValidInput(self):
        # Test with valid integer input
        stringValue = 680
        expectedOutput = 680

        result = self.Commands.convertToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to match the input integer value")

    def test_convertToInt_InvalidInput(self):
        # Test with invalid input (non-numeric string)
        stringValue = "abc"
        expectedOutput = None

        result = self.Commands.convertToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to be None for invalid input")

    def test_convertWordToInt_InvalidInput(self):
        # Test with invalid input (neither integer nor string)
        stringValue = 3.14
        expectedOutput = None

        result = self.Commands.convertWordToInt(stringValue)
        self.assertEqual(result, expectedOutput, "Expected output to be None for invalid input")

class testSetVolumeMethods(unittest.TestCase):
    def setUp(self):
        self.Commands = operations()

    def test_setVolumeTo0(self):
        volChoice = 0
        decibel = -40
        expectedOutput = "Successfully set volume to 0"
        errorMessage = "Set volume to 0 does not match expected output"

        result = self.Commands.setVolume(volChoice, decibel)
        self.assertEqual(result, expectedOutput, errorMessage)

    def test_setVolumeTo30(self):
        volChoice = 30
        decibel = -17.8
        expectedOutput = "Successfully set volume to 30"
        errorMessage = "Set volume to 30 does not match expected output"

        result = self.Commands.setVolume(volChoice, decibel)
        self.assertEqual(result, expectedOutput, errorMessage)

    def test_setVolumeTo100(self):
        volChoice = 100
        decibel = 0
        expectedOutput = "Successfully set volume to 100"
        errorMessage = "Set volume to 100 does not match expected output"

        result = self.Commands.setVolume(volChoice, decibel)
        self.assertEqual(result, expectedOutput, errorMessage)

    def test_setVolume_InvalidInput(self):
        volChoice = "INVALID_VOLCHOICE"
        decibel = "INVALID_DECIBEL"
        expectedOutput = "An exception occured while setting volume to INVALID_VOLCHOICE"
        errorMessage = "Set volume with invalid inputs does not match expected output"

        result = self.Commands.setVolume(volChoice, decibel)
        self.assertEqual(result, expectedOutput, errorMessage)

class testSearchDocumentMethods(unittest.TestCase):
    def setUp(self):
        self.Commands = operations()

    @patch("source.core.command_module.pyautogui.click")
    @patch("source.core.command_module.pyautogui.typewrite")
    @patch("source.core.command_module.pyautogui.press")
    def test_searchForDocument_ValidInput(self, mock_pyautogui_click,
                                                mock_pyautogui_typewrite,
                                                mock_pyautogui_press):
        docChoice = "lab 6"
        expectedOutput = "Successful search for Document: lab 6"
        errorMessage = "Search for document with valid input does not match expected output"

        mock_pyautogui_click.return_value = None
        mock_pyautogui_typewrite.return_value = None
        mock_pyautogui_press.return_value = None

        result = self.Commands.searchForDocument(docChoice)
        self.assertEqual(result, expectedOutput, errorMessage)

    def test_searchForDocument_InvalidInput(self):
        docChoice = 0
        expectedOutput = "Invalid document: 0"
        errorMessage = "Search for document with invalid input does not match expected output"

        result = self.Commands.searchForDocument(docChoice)
        self.assertEqual(result, expectedOutput, errorMessage)


if __name__ == '__main__':
    unittest.main()
