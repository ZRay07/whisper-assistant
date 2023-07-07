import unittest
from source.core.command_module import openApplication, closeApplication
from source.core.command_module import scrollUp, scrollDown
from source.core.command_module import setVolume


class testApplicationMethods(unittest.TestCase):
    def test_openApp(self):
        self.assertTrue(openApplication("Word"), 
                        "Expected succesful app opening")
        
    def test_openFalseApp(self):
        self.assertFalse(openApplication("APPNAME"),
                         "Expected failed app opening")
        
    def test_closeApp(self):
        self.assertTrue(closeApplication("Spotify"), 
                        "Expected succesful app closing")

    def test_closeFalseApp(self):
        self.assertFalse(closeApplication("APPNAME"),
                         "Expected failed app closing")

class testScrollMethods(unittest.TestCase):
    def test_scrollUp(self):
        self.assertTrue(scrollUp(10),
                        "Expected scroll up by 10 'clicks'")
        
    def test_falseScrollUp(self):
        self.assertFalse(scrollUp("A"),
                         "Expected failed scrolling up")
        
    def test_scrollDown(self):
        self.assertTrue(scrollDown(-10),
                        "Expected scroll down by 10 'clicks'")
        
    def test_falseScrollDown(self):
        self.assertFalse(scrollUp("A"),
                         "Expected failed scrolling down")
        
class testSetVolumeMethods(unittest.TestCase):
    def test_setVolumeTo0(self):
        self.assertEqual(0, setVolume("0"), 
                         "Expected volume to be set to 0.")

if __name__ == '__main__':
    unittest.main()