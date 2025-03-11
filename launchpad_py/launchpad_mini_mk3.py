from pygame import time

from launchpad_py import LaunchpadPro

__all__ = ['LaunchpadMiniMk3']


class LaunchpadMiniMk3(LaunchpadPro):
    """
    For 3-color "Mk3" Launchpads; Mini and Pro

    LED AND BUTTON NUMBERS IN RAW MODE (DEC)


           +---+---+---+---+---+---+---+---+  +---+
           |104|   |106|   |   |   |   |111|  |112|
           +---+---+---+---+---+---+---+---+  +---+

           +---+---+---+---+---+---+---+---+  +---+
           | 81|   |   |   |   |   |   |   |  | 89|
           +---+---+---+---+---+---+---+---+  +---+
           | 71|   |   |   |   |   |   |   |  | 79|
           +---+---+---+---+---+---+---+---+  +---+
           | 61|   |   |   |   |   | 67|   |  | 69|
           +---+---+---+---+---+---+---+---+  +---+
           | 51|   |   |   |   |   |   |   |  | 59|
           +---+---+---+---+---+---+---+---+  +---+
           | 41|   |   |   |   |   |   |   |  | 49|
           +---+---+---+---+---+---+---+---+  +---+
           | 31|   |   |   |   |   |   |   |  | 39|
           +---+---+---+---+---+---+---+---+  +---+
           | 21|   | 23|   |   |   |   |   |  | 29|
           +---+---+---+---+---+---+---+---+  +---+
           | 11|   |   |   |   |   |   |   |  | 19|
           +---+---+---+---+---+---+---+---+  +---+



    LED AND BUTTON NUMBERS IN XY MODE (X/Y)

             0   1   2   3   4   5   6   7      8
           +---+---+---+---+---+---+---+---+  +---+
           |0/0|   |2/0|   |   |   |   |   |  |8/0|  0
           +---+---+---+---+---+---+---+---+  +---+

           +---+---+---+---+---+---+---+---+  +---+
           |0/1|   |   |   |   |   |   |   |  |   |  1
           +---+---+---+---+---+---+---+---+  +---+
           |   |   |   |   |   |   |   |   |  |   |  2
           +---+---+---+---+---+---+---+---+  +---+
           |   |   |   |   |   |5/3|   |   |  |   |  3
           +---+---+---+---+---+---+---+---+  +---+
           |   |   |   |   |   |   |   |   |  |   |  4
           +---+---+---+---+---+---+---+---+  +---+
           |   |   |   |   |   |   |   |   |  |   |  5
           +---+---+---+---+---+---+---+---+  +---+
           |   |   |   |   |4/6|   |   |   |  |   |  6
           +---+---+---+---+---+---+---+---+  +---+
           |   |   |   |   |   |   |   |   |  |   |  7
           +---+---+---+---+---+---+---+---+  +---+
           |   |   |   |   |   |   |   |   |  |8/8|  8
           +---+---+---+---+---+---+---+---+  +---+
    """

    #	COLORS = {'black':0, 'off':0, 'white':3, 'red':5, 'green':17 }

    def Open(self, number=0, name="MiniMK3"):
        """
        Opens one of the attached Launchpad MIDI devices.
        Uses search string "MiniMk3", by default.
        """
        retval = super(LaunchpadMiniMk3, self).Open(number=number, name=name)
        if retval == True:
            self.LedSetMode(1)

        return retval

    def Check(self, number=0, name="MiniMK3"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "MiniMk3", by default.
        """
        return super(LaunchpadMiniMk3, self).Check(number=number, name=name)

    # TODO: ASkr, Undocumented!
    # TODO: return value
    def LedSetLayout(self, mode):
        """
        Sets the button layout (and codes) to the set, specified by <mode>.
        Valid options:
         00 - Session, 04 - Drums, 05 - Keys, 06 - User (Drum)
         0D - DAW Faders (available if Session enabled), 7F - Programmer
        Until now, we'll need the "Session" (0x00) settings.
        """
        ValidModes = [0x00, 0x04, 0x05, 0x06, 0x0d, 0x7F]
        if mode not in ValidModes:
            return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 13, 0, mode])
        time.wait(10)

    def LedSetMode(self, mode):
        """
        Selects the Mk3's mode.
        <mode> -> 0 -> "Ableton Live mode"
                  1 -> "Programmer mode"	(what we need)
        """
        if mode < 0 or mode > 1:
            return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 13, 14, mode])
        time.wait(10)

    # TODO: ASkr, Undocumented!
    def LedSetButtonLayoutSession(self):
        """
        Sets the button layout to "Session" mode.
        """
        self.LedSetLayout(0)

    def LedCtrlRaw(self, number, red, green, blue=None):
        """
        Controls a grid LED by its position <number> and a color, specified by
        <red>, <green> and <blue> intensities, with can each be an integer between 0..63.
        If <blue> is omitted, this method runs in "Classic" compatibility mode and the
        intensities, which were within 0..3 in that mode, are multiplied by 21 (0..63)
        to emulate the old brightness feeling :)
        Notice that each message requires 10 bytes to be sent. For a faster, but
        unfortunately "not-RGB" method, see "LedCtrlRawByCode()"
        Mk3 color data extended to 7-bit but for compatibility we are still using 6-bit values
        """

        if number < 0 or number > 99:
            return

        if blue is None:
            blue = 0
            red *= 21
            green *= 21

        limit = lambda n, mini, maxi: max(min(maxi, n), mini)

        red = limit(red, 0, 63) << 1
        green = limit(green, 0, 63) << 1
        blue = limit(blue, 0, 63) << 1

        self.midi.RawWriteSysEx([0, 32, 41, 2, 13, 3, 3, number, red, green, blue])

    def LedCtrlPulseByCode(self, number, colorcode=None):
        """
        Same as LedCtrlRawByCode, but with a pulsing LED.
        Pulsing can be stopped by another Note-On/Off or SysEx message.
        """

        if number < 0 or number > 99:
            return

        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']

        colorcode = min(127, max(0, colorcode))

        self.midi.RawWrite(146, number, colorcode)

    def LedCtrlFlashByCode(self, number, colorcode=None):
        """
        Same as LedCtrlPulseByCode, but with a dual color flashing LED.
        The first color is the one that is already enabled, the second one is the
        <colorcode> argument in this method.
        Flashing can be stoppped by another Note-On/Off or SysEx message.
        """

        if number < 0 or number > 99:
            return

        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']

        colorcode = min(127, max(0, colorcode))

        self.midi.RawWrite(145, number, colorcode)

    def LedAllOn(self, colorcode=None):
        """
        Quickly sets all LEDs to the same color, given by <colorcode>.
        If <colorcode> is omitted, "white" is used.
        """

        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']

        colorcode = min(127, max(0, colorcode))

        # TODO: Maybe the SysEx was indeed a better idea :)
        #       Did some tests:
        #         MacOS:   doesn't matter;
        #         Windoze: SysEx much better;
        #         Linux:   completely freaks out
        for x in range(9):
            for y in range(9):
                self.midi.RawWrite(144, (x + 1) + ((y + 1) * 10), colorcode)

    def Reset(self):
        """
        (fake to) reset the Launchpad
        Turns off all LEDs
        """
        self.LedAllOn(0)

    def Close(self):
        """
        Go back to custom modes before closing connection
        Otherwise Launchpad will stuck in programmer mode
        """
        # removed for now (LEDs would light up again; should be in the user's code)
        #		self.LedSetLayout( 0x05 )

        # TODO: redundant (but needs fix for Py2 embedded anyway)
        self.midi.CloseInput()
        self.midi.CloseOutput()
