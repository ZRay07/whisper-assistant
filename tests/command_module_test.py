import unittest
import AppOpener
from source.core.command_module import openApplication

class testApplicationMethods(unittest.TestCase):

    def test_openApp(self):
        self.assertTrue(openApplication("Word"), 
                        "Expected succesful app opening")
        
    def test_openFalseApp(self):
        self.assertFalse(openApplication("APPNAME"),
                         "Expected failed app opening")

    def test_closeFalseApp(self):
        with self.assertRaises(Exception):
            AppOpener.close("APPNAME", throw_error = True)



if __name__ == '__main__':
    unittest.main()