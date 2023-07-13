import unittest
from source.core.model_interface import Recorder, ASR_model, RECORD_PATH

class TestModelInterface(unittest.TestCase):

    def setUp(self):
        self.recorder = Recorder()
        self.asr_model = ASR_model()

    def tearDown(self):
        pass

    def test_audio_recording(self):
        # Test if audio recording is successful
        record_duration = 1
        self.assertTrue(self.recorder.record(record_duration))

    def test_model_loading(self):
        # Test if ASR model and processor are loaded successfully
        self.assertTrue(self.asr_model)

    def test_transcription(self):
        # Test the transcription functionality
        transcription = self.asr_model.use_model(RECORD_PATH)
        self.assertIsNotNone(transcription)
        self.assertIsInstance(transcription, str)

if __name__ == "__main__":
    unittest.main()
