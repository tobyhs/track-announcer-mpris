import dbus
from mpris2 import Player, get_players_uri

from .speaker import Speaker

class PropertiesChangedHandler:
    """Handler for PropertiesChanged D-Bus signals with a path of /org/mpris/MediaPlayer2.
    """

    def __init__(self, speaker: Speaker):
        """
        Args:
            speaker: object to speak text
        """
        self.speaker = speaker

    def handle(
        self,
        interface: dbus.String,
        changed_properties: dbus.Dictionary,
        invalidated_properties: dbus.Array
    ) -> None:
        """Handles a media player property change from D-Bus.

        This speaks the media's title when the title changes and the media
        player is playing.

        Args:
            interface: D-Bus interface name
            changed_properties: properties that changed with their new values
            invalidated_properties: properties that changed where the values
                were not conveyed
        """
        try:
            title = changed_properties['Metadata']['xesam:title']
        except KeyError:
            return

        player_uri = next(get_players_uri())
        player = Player(dbus_interface_info={'dbus_uri': player_uri})
        if player.PlaybackStatus == 'Playing':
            player.Pause()
            self.speaker.speak(title)
            player.Play()
