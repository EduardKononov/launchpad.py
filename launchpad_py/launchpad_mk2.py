from launchpad_py import LaunchpadPro

__all__ = ['LaunchpadMk2']


class LaunchpadMk2(LaunchpadPro):
    """
    For 3-color "Mk2" Launchpads with 8x8 matrix and 2x8 right/top rows

    LED AND BUTTON NUMBERS IN RAW MODE (DEC)

    Notice that the fine manual doesn't know that mode.
    According to what's written there, the numbering used
    refers to the "PROGRAMMING MODE", which actually does
    not react to any of those notes (or numbers).

           +---+---+---+---+---+---+---+---+
           |104|   |106|   |   |   |   |111|
           +---+---+---+---+---+---+---+---+

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
           +---+---+---+---+---+---+---+---+
           |0/0|   |2/0|   |   |   |   |   |         0
           +---+---+---+---+---+---+---+---+

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

    def Open(self, number=0, name="Mk2"):
        """
        Opens one of the attached Launchpad MIDI devices.
        Uses search string "Mk2", by default.
        """
        return super(LaunchpadMk2, self).Open(number=number, name=name)

    def Check(self, number=0, name="Mk2"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "Mk2", by default.
        """
        return super(LaunchpadMk2, self).Check(number=number, name=name)

    def LedAllOn(self, colorcode=None):
        """
        Quickly sets all LEDs to the same color, given by <colorcode>.
        If <colorcode> is omitted, "white" is used.
        """

        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']
        else:
            colorcode = min(colorcode, 127)
            colorcode = max(colorcode, 0)

        self.midi.RawWriteSysEx([0, 32, 41, 2, 24, 14, colorcode])

    def Reset(self):
        """
        (fake to) reset the Launchpad
        Turns off all LEDs
        """
        self.LedAllOn(0)

    def ButtonStateXY(self):
        """
        Returns the raw value of the last button change (pressed/unpressed) as a list
        [ <x>, <y>, <value> ], in which <x> and <y> are the buttons coordinates and
        <svalue> the intensity. Because the Mk2 does not come with full analog capabilities,
        unlike the "Pro", the intensity values for the "Mk2" are either 0 or 127.
        127 = button pressed; 0 = button released
        Notice that this is not (directly) compatible with the original ButtonStateRaw()
        method in the "Classic" Launchpad, which only returned [ <button>, <True/False> ].
        Compatibility would require checking via "== True" and not "is True".
        """

        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            if a[0][0][0] == 144 or a[0][0][0] == 176:

                if a[0][0][1] >= 104:
                    x = a[0][0][1] - 104
                    y = 0
                else:
                    x = (a[0][0][1] - 1) % 10
                    y = (99 - a[0][0][1]) // 10

                return [x, y, a[0][0][2]]
            else:
                return []
        else:
            return []

    def LedCtrlRaw(self, number, red, green, blue=None):
        """
        Controls a grid LED by its position <number> and a color, specified by
        <red>, <green> and <blue> intensities, with can each be an integer between 0..63.
        If <blue> is omitted, this methos runs in "Classic" compatibility mode and the
        intensities, which were within 0..3 in that mode, are multiplied by 21 (0..63)
        to emulate the old brightness feeling :)
        Notice that each message requires 10 bytes to be sent. For a faster, but
        unfortunately "not-RGB" method, see "LedCtrlRawByCode()"
        """

        number = min(number, 111)
        number = max(number, 0)

        if number > 89 and number < 104:
            return

        if blue is None:
            blue = 0
            red *= 21
            green *= 21

        limit = lambda n, mini, maxi: max(min(maxi, n), mini)

        red = limit(red, 0, 63)
        green = limit(green, 0, 63)
        blue = limit(blue, 0, 63)

        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 11, number, red, green, blue])

    def LedCtrlRawByCode(self, number, colorcode=None):
        """
        Controls a grid LED by its position <number> and a color code <colorcode>
        from the Launchpad's color palette.
        If <colorcode> is omitted, 'white' is used.
        This method should be ~3 times faster that the RGB version "LedCtrlRaw()", which
        uses 10 byte, system-exclusive MIDI messages.
        """

        number = min(number, 111)
        number = max(number, 0)

        if number > 89 and number < 104:
            return

        # TODO: limit/check colorcode
        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']

        if number < 104:
            self.midi.RawWrite(144, number, colorcode)
        else:
            self.midi.RawWrite(176, number, colorcode)

    def LedCtrlPulseByCode(self, number, colorcode=None):
        """
        Same as LedCtrlRawByCode, but with a pulsing LED.
        Pulsing can be stoppped by another Note-On/Off or SysEx message.
        """

        if number < 0 or number > 99:
            return

        # TODO: limit/check colorcode
        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']

        # for Pro: [ 0, 32, 41, 2, *16*, 40, number, colorcode ]
        # Also notice the error in the Mk2 docs. "number" is actually the 2nd
        # command, following an unused "0" (that's also missing in the Pro's command)
        self.midi.RawWriteSysEx([0, 32, 41, 2, 24, 40, 0, number, colorcode])

    def LedCtrlFlashByCode(self, number, colorcode=None):
        """
        Same as LedCtrlPulseByCode, but with a dual color flashing LED.
        The first color is the one that is already enabled, the second one is the
        <colorcode> argument in this method.
        Flashing can be stoppped by another Note-On/Off or SysEx message.
        """

        if number < 0 or number > 99:
            return

        # TODO: limit/check colorcode
        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']

        # for Pro: [ 0, 32, 41, 2, *16*, *35*, number, colorcode ] (also an error in the docs)
        self.midi.RawWriteSysEx([0, 32, 41, 2, 24, 35, 0, number, colorcode])

    def LedCtrlXY(self, x, y, red, green, blue=None):
        """
        Controls a grid LED by its coordinates <x>, <y> and <reg>, <green> and <blue>
        intensity values.
        This method internally uses "LedCtrlRaw()".
        Please also notice the comments in that one.
        """

        if x < 0 or x > 8 or y < 0 or y > 8:
            return

        # top row (round buttons)
        if y == 0:
            led = 104 + x
        else:
            # swap y
            led = 91 - (10 * y) + x

        self.LedCtrlRaw(led, red, green, blue)

    def LedCtrlXYByRGB(self, x, y, lstColor):
        """
        New approach to color arguments.
        Controls a grid LED by its coordinates <x>, <y> and a list of colors <lstColor>.
        <lstColor> is a list of length 3, with RGB color information, [<r>,<g>,<b>]
        """

        if type(lstColor) is not list or len(lstColor) < 3:
            return

        if x < 0 or x > 8 or y < 0 or y > 8:
            return

        # top row (round buttons)
        if y == 0:
            led = 104 + x
        else:
            # swap y
            led = 91 - (10 * y) + x

        self.LedCtrlRaw(led, lstColor[0], lstColor[1], lstColor[2])

    def LedCtrlXYByCode(self, x, y, colorcode):
        """
        Controls a grid LED by its coordinates <x>, <y> and its <colorcode>.
        About three times faster than the, indeed much more comfortable RGB version
        "LedCtrlXY()"
        """

        if x < 0 or x > 8 or y < 0 or y > 8:
            return

        # top row (round buttons)
        if y == 0:
            led = 104 + x
        else:
            # swap y
            led = 91 - (10 * y) + x

        self.LedCtrlRawByCode(led, colorcode)

    def LedCtrlPulseXYByCode(self, x, y, colorcode):
        """
        Pulses a grid LED by its coordinates <x>, <y> and its <colorcode>.
        """

        if x < 0 or x > 8 or y < 0 or y > 8:
            return

        # top row (round buttons)
        if y == 0:
            led = 104 + x
        else:
            # swap y
            led = 91 - (10 * y) + x

        self.LedCtrlPulseByCode(led, colorcode)

    def LedCtrlFlashXYByCode(self, x, y, colorcode):
        """
        Flashes a grid LED by its coordinates <x>, <y> and its <colorcode>.
        """

        if x < 0 or x > 8 or y < 0 or y > 8:
            return

        # top row (round buttons)
        if y == 0:
            led = 104 + x
        else:
            # swap y
            led = 91 - (10 * y) + x

        self.LedCtrlFlashByCode(led, colorcode)
