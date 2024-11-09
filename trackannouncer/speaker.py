from abc import ABC, abstractmethod
import shlex
import subprocess
from typing import override

class Speaker(ABC):
    """Abstract class for speaking given text."""

    @abstractmethod
    def speak(self, text: str) -> None:
        """Speaks the given text.

        Args:
            text: text to speak
        Raises: SpeakError: if speaking fails
        """
        pass

class SpeakError(Exception):
    """An exception raised when Speaker.speak fails."""
    pass

class SubprocessSpeaker(Speaker):
    """A Speaker that launches a process to speak."""

    def __init__(self, command_template: str):
        """
        Args:
            command_template: the command to run; use %s as a placeholder for
                the text to speak
        """
        self._argv_template = shlex.split(command_template)

    @override
    def speak(self, text: str) -> None:
        argv = [text if arg == '%s' else arg for arg in self._argv_template]
        process = subprocess.run(argv, stderr=subprocess.PIPE)
        if process.returncode != 0:
            raise SpeakError(process.stderr.decode())
