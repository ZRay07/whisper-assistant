from source.ui.ui import InputValidation
from source.core.command_module import loadValidApps

import unittest
import json
import os

class testAppValidation(unittest.TestCase):
    def setUp(self):
        self.InputValidator = InputValidation()

        # Create a mock JSON file with some app names
        self.app_data = {
            "word": "C:/Program Files/Microsoft Office/Word.exe",
            "excel": "C:/Program Files/Microsoft Office/Excel.exe",
            "powerPoint": "C:/Program Files/Microsoft Office/PowerPoint.exe",
            "chrome": "C:/Program Files/Google/Chrome.exe"
        }

        # Save the mock data to a JSON file
        with open("data/app_data.json", "w") as json_file:
            json.dump(self.app_data, json_file)

        # Explicitly close the file
        json_file.close()

        self.validApps = loadValidApps()

    def tearDown(self):
        self.InputValidator.root.destroy()
        del self.InputValidator

        # Clean up the mock JSON file
        os.remove("data/app_data.json")

    def test_ValidateOpenAppName_ValidAppName(self):
        app_name = "word"
        action = "open"
        expected_output = "word"
        errorMessage = "App name validation with valid input does not produce expected output"

        result = self.InputValidator.validateAppInput(app_name, action, self.validApps)
        self.assertEqual(result, expected_output, errorMessage)

    def test_ValidateOpenAppName_InvalidAppName(self):
        app_name = "INVALID_APPNAME"
        action = "open"
        expected_output = False
        error_message = "App name validation with invalid input does not produce expected output"

        result = self.InputValidator.validateAppInput(app_name, action, self.validApps)
        self.assertEqual(result, expected_output, error_message)  

    def test_ValidateCloseAppName_ValidAppName(self):
        app_name = "word"
        action = "close"
        expected_output = "word"
        errorMessage = "App name validation with valid input does not produce expected output"

        result = self.InputValidator.validateAppInput(app_name, action, self.validApps)
        self.assertEqual(result, expected_output, errorMessage)

    def test_ValidateCloseAppName_InvalidAppName(self):
        app_name = "INVALID_APPNAME"
        action = "close"
        expected_output = False
        error_message = "App name validation with invalid input does not produce expected output"

        result = self.InputValidator.validateAppInput(app_name, action, self.validApps)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateOpenAppName_InvalidAction(self):
        app_name = "word"
        action = "INVALID_ACTION"
        expected_output = False
        error_message = "App name validation with invalid action does not produce expected output"

        result = self.InputValidator.validateAppInput(app_name, action, self.validApps)
        self.assertEqual(result, expected_output, error_message)


class testScrollValidation(unittest.TestCase):
    def setUp(self):
        self.InputValidator = InputValidation()

    def tearDown(self):
        self.InputValidator.root.destroy()
        del self.InputValidator

    def test_ValidateDefaultScrollUp(self):
        scroll_amount = "up"
        expected_output = 100
        error_message = "Default scroll up validation does not produce expected output"

        result = self.InputValidator.validateScrollInput(scroll_amount)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateDefaultScrollDown(self):
        scroll_amount = "down"
        expected_output = 100
        error_message = "Default scroll up validation does not produce expected output"

        result = self.InputValidator.validateScrollInput(scroll_amount)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateScrollAmount_ValidInput(self):
        scroll_amount = 500
        expected_output = 500
        error_message = "Scroll up validation with valid input does not produce expected output"

        result = self.InputValidator.validateScrollInput(scroll_amount)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateScrollAmount_ValidWordInput(self):
        scroll_amount = "two hundred"
        expected_output = 200
        error_message = "Scroll up validation with valid word input does not produce expected output"

        result = self.InputValidator.validateScrollInput(scroll_amount)
        self.assertEqual(result, expected_output, error_message)

    @unittest.skip("Skipped because prompted for user input.")
    def test_ValidateScrollAmount_InvalidInput(self):
        scroll_amount = "INVALID_NUMBER"
        expected_output = " "
        error_message = "Scroll up validation with valid word input does not produce expected output"

        result = self.InputValidator.validateScrollInput(scroll_amount)
        self.assertEqual(result, expected_output, error_message)



class testVolumeValidation(unittest.TestCase):
    def setUp(self):
        self.InputValidator = InputValidation()

    def tearDown(self):
        self.InputValidator.root.destroy()
        del self.InputValidator

    @unittest.skip("Skipped because prompted for user input.")
    def test_ValidateDefaultVolume(self):
        vol_choice = "volume"
        expected_output = " "
        error_message = "Default volume validation does not produce expected output"

        result = self.InputValidator.validateVolumeInput(vol_choice)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateVolume_ValidInput_0(self):
        vol_choice = 0
        expected_output = (0, -60.0)
        error_message = "Volume validation with 0 as input does not produce expected output"

        result = self.InputValidator.validateVolumeInput(vol_choice)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateVolume_ValidInput_10(self):
        vol_choice = 10
        expected_output = (10, -33.0)
        error_message = "Volume validation with 10 as input does not produce expected output"

        result = self.InputValidator.validateVolumeInput(vol_choice)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateVolume_ValidInput_20(self):
        vol_choice = 20
        expected_output = (20, -23.4)
        error_message = "Volume validation with 20 as input does not produce expected output"

        result = self.InputValidator.validateVolumeInput(vol_choice)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateVolume_ValidInput_30(self):
        vol_choice = 30
        expected_output = (30, -17.8)
        error_message = "Volume validation with 30 as input does not produce expected output"

        result = self.InputValidator.validateVolumeInput(vol_choice)
        self.assertEqual(result, expected_output, error_message)

    def test_ValidateVolume_ValidInput_100(self):
        vol_choice = 100
        expected_output = (100, 0)
        error_message = "Volume validation with 100 as input does not produce expected output"

        result = self.InputValidator.validateVolumeInput(vol_choice)
        self.assertEqual(result, expected_output, error_message)

    @unittest.skip("Skipped because prompted for user input.")
    def test_ValidateVolume_InvalidInput(self):
        vol_choice = "INVALID_VOLUME"
        expected_output = " "
        error_message = "Volume validation with 'INVALID_VOLUME' as input does not produce expected output"

        result = self.InputValidator.validateVolumeInput(vol_choice)
        self.assertEqual(result, expected_output, error_message)



class testDocumentValidation(unittest.TestCase):
    def setUp(self):
        self.InputValidator = InputValidation()

    def tearDown(self):
        self.InputValidator.root.destroy()
        del self.InputValidator

    @unittest.skip("Skipped because prompted for user input.")
    def test_ValidateDefaultDocument(self):
        doc_choice = "search for a document"
        expected_output = " "
        error_message = "Default document validation does not produce expected output"

        result = self.InputValidator.validateDocumentInput(doc_choice)
        self.assertEqual(result, expected_output, error_message)

    def test_validateDocumentSearch_ValidInput(self):
        doc_choice = "search for a document lab 6"
        expected_output = "lab 6"
        error_message = "Document validation with valid input does not produce expected output"

        result = self.InputValidator.validateDocumentInput(doc_choice, askToConfirm=False)
        self.assertEqual(result, expected_output, error_message)



    









if __name__ == '__main__':
    unittest.main()
