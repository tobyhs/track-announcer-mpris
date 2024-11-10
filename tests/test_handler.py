import dbus
from unittest import TestCase, mock

from trackannouncer.handler import PropertiesChangedHandler
from trackannouncer.speaker import Speaker

class PropertiesChangedHandlerTest(TestCase):
    PLAYER_URI = dbus.String('org.mpris.MediaPlayer2.TestPlayer')
    INTERFACE = dbus.String('org.mpris.MediaPlayer2.Player')
    INVALIDATED_PROPERTIES = dbus.Array([], signature=dbus.Signature('s'))

    def setUp(self):
        self.speaker = mock.create_autospec(Speaker, instance=True)
        self.handler = PropertiesChangedHandler(self.speaker)

        self.addCleanup(mock.patch.stopall)
        self.player_class_mock = mock.patch(
            'trackannouncer.handler.Player'
        ).start()
        self.player = self.player_class_mock()
        self.player_class_mock.reset_mock()
        self.get_players_uri_mock = mock.patch(
            'trackannouncer.handler.get_players_uri', autospec=True
        ).start()
        self.get_players_uri_mock.return_value = (
            uri for uri in [self.PLAYER_URI]
        )

    def test_handle_no_title_change(self):
        props = dbus.Dictionary({
            dbus.String('PlaybackStatus'): dbus.String('Playing'),
        })
        self.handler.handle(self.INTERFACE, props, self.INVALIDATED_PROPERTIES)

        self.get_players_uri_mock.assert_not_called()
        self.player_class_mock.assert_not_called()

    def test_handle_title_change_but_not_playing(self):
        self.player.PlaybackStatus = 'Paused'
        props = dbus.Dictionary({
            dbus.String('Metadata'): dbus.Dictionary({
                dbus.String('xesam:title'): dbus.String('Track Title'),
            }),
        })
        self.handler.handle(self.INTERFACE, props, self.INVALIDATED_PROPERTIES)

        self.player.Pause.assert_not_called()
        self.speaker.speak.assert_not_called()
        self.player.Play.assert_not_called()

    def test_handle_title_change_and_playing(self):
        self.player.PlaybackStatus = 'Playing'
        props = dbus.Dictionary({
            dbus.String('Metadata'): dbus.Dictionary({
                dbus.String('xesam:title'): dbus.String('Track Title'),
            }),
        })
        self.handler.handle(self.INTERFACE, props, self.INVALIDATED_PROPERTIES)

        self.player_class_mock.assert_called_with(
            dbus_interface_info={'dbus_uri': self.PLAYER_URI}
        )
        self.player.Pause.assert_called_once()
        self.speaker.speak.assert_called_once_with('Track Title')
        self.player.Play.assert_called_once()
