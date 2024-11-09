import subprocess
from unittest import TestCase, mock

from trackannouncer.speaker import SpeakError, SubprocessSpeaker

class SubprocessSpeakerTest(TestCase):
    def test_speak(self):
        process = mock.create_autospec(
            subprocess.CompletedProcess, instance=True
        )
        process.returncode = 0
        speaker = SubprocessSpeaker('speak "Next Track" %s')
        with mock.patch('trackannouncer.speaker.subprocess.run') as run_mock:
            run_mock.return_value = process
            speaker.speak('Track Title')
            run_mock.assert_called_with(
                ['speak', 'Next Track', 'Track Title'], stderr=subprocess.PIPE
            )

    def test_speak_error(self):
        process = mock.create_autospec(
            subprocess.CompletedProcess, instance=True
        )
        process.returncode = 1
        process.stderr = b'Some error'
        speaker = SubprocessSpeaker('speak %s')
        with mock.patch('trackannouncer.speaker.subprocess.run') as run_mock:
            run_mock.return_value = process
            with self.assertRaises(SpeakError) as cm:
                speaker.speak('Other Title')
            self.assertEqual(cm.exception.args, ('Some error',))
            run_mock.assert_called_with(
                ['speak', 'Other Title'], stderr=subprocess.PIPE
            )
