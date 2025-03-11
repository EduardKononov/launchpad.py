from pygame import time

from launchpad_py.midi import Midi

__all__ = ['LaunchpadBase']


class LaunchpadBase(object):
    def __init__(self):
        self.midi = Midi()  # midi interface instance (singleton)
        self.idOut = None  # midi id for output
        self.idIn = None  # midi id for input

        # scroll directions
        self.SCROLL_NONE = 0
        self.SCROLL_LEFT = -1
        self.SCROLL_RIGHT = 1

    def __del__(self):
        self.Close()

    def Open(self, number=0, name="Launchpad"):
        """
        Opens one of the attached Launchpad MIDI devices.
        """

        self.idOut = self.midi.SearchDevice(name, True, False, number=number)
        self.idIn = self.midi.SearchDevice(name, False, True, number=number)

        if self.idOut is None or self.idIn is None:
            return False

        if not self.midi.OpenOutput(self.idOut):
            return False

        return self.midi.OpenInput(self.idIn)

    def Check(self, number=0, name="Launchpad"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        """

        self.idOut = self.midi.SearchDevice(name, True, False, number=number)
        self.idIn = self.midi.SearchDevice(name, False, True, number=number)

        if self.idOut is None or self.idIn is None:
            return False

        return True

    def Close(self):
        """
        Closes this device
        """

        self.midi.CloseInput()
        self.midi.CloseOutput()

    def ListAll(self, searchString=''):
        """
        Prints a list of all devices to the console (for debug)
        """

        self.midi.SearchDevices(searchString, True, True, False)

    def ButtonFlush(self):
        """
        Clears the button buffer (The Launchpads remember everything...)
        Because of empty reads (timeouts), there's nothing more we can do here, but
        repeat the polls and wait a little...
        """

        n_attempts = 0
        n_retries = 3
        while n_attempts < n_retries:
            if self.midi.ReadCheck():
                n_attempts = 0
                self.midi.ReadRaw()
            else:
                n_attempts += 1
                time.wait(5)

    def EventRaw(self):
        """
        Returns a list of all MIDI events, empty list if nothing happened.
        Useful for debugging or checking new devices.
        """
        if self.midi.ReadCheck():
            return self.midi.ReadRaw()
        else:
            return []
