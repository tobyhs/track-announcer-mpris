import argparse
import dbus
from gi.repository import GLib

from .handler import PropertiesChangedHandler
from .speaker import SubprocessSpeaker

class Runner:
    """Main command line runner"""

    def __init__(self, bus: dbus.bus.BusConnection, loop: GLib.MainLoop):
        """
        Args:
            bus: D-Bus session bus
            loop: event loop to run signal callbacks
        """
        self.bus = bus
        self.loop = loop

        self.arg_parser = argparse.ArgumentParser(allow_abbrev=False)
        self.arg_parser.add_argument(
            '-s', '--speak-command-template',
            default='speak %s',
            help='the command to run; use %%s as a placeholder for the text to speak'
        )

    def run(self, args: list[str]) -> None:
        """Runs the program.

        Args:
            args: command line arguments (excluding the program)
        """
        namespace = self.arg_parser.parse_args(args)
        speaker = SubprocessSpeaker(namespace.speak_command_template)
        handler = PropertiesChangedHandler(speaker)
        signal_match = self.bus.add_signal_receiver(
            handler.handle,
            dbus_interface='org.freedesktop.DBus.Properties',
            signal_name='PropertiesChanged',
            path='/org/mpris/MediaPlayer2'
        )
        try:
            self.loop.run()
        finally:
            signal_match.remove()
