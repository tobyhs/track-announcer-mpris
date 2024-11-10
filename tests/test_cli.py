import dbus
from gi.repository import GLib
from unittest import TestCase, mock

from trackannouncer.cli import Runner

class RunnerTest(TestCase):
    def setUp(self):
        self.bus = mock.create_autospec(dbus.bus.BusConnection, instance=True)
        self.loop = mock.create_autospec(GLib.MainLoop, instance=True)
        self.runner = Runner(self.bus, self.loop)

        self.addCleanup(mock.patch.stopall)
        self.speaker_class_mock = mock.patch(
            'trackannouncer.cli.SubprocessSpeaker', autospec=True
        ).start()
        self.handler_class_mock = mock.patch(
            'trackannouncer.cli.PropertiesChangedHandler', autospec=True
        ).start()

    def test_run_with_no_options(self):
        self.runner.run([])
        self._check_run('speak %s')

    def test_run_with_short_options(self):
        speak_command_template = 'custom-speak Next Track %s'
        self.runner.run(['-s', speak_command_template])
        self._check_run(speak_command_template)

    def test_run_with_long_options(self):
        speak_command_template = 'custom-speak --some-option %s'
        self.runner.run(['--speak-command-template', speak_command_template])
        self._check_run(speak_command_template)

    def _check_run(self, speak_command_template: str) -> None:
        self.speaker_class_mock.assert_called_once_with(speak_command_template)
        self.handler_class_mock.assert_called_once_with(
            self.speaker_class_mock.return_value
        )
        self.bus.add_signal_receiver.assert_called_once_with(
            self.handler_class_mock.return_value.handle,
            dbus_interface='org.freedesktop.DBus.Properties',
            signal_name='PropertiesChanged',
            path='/org/mpris/MediaPlayer2'
        )
        self.loop.run.assert_called_once()
        self.bus.add_signal_receiver.return_value.remove.assert_called_once()
