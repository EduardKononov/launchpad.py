from pygame import time

from launchpad_py.charset import CHARTAB
from launchpad_py.launchpad_base import LaunchpadBase

__all__ = ['LaunchpadPro']


class LaunchpadPro(LaunchpadBase):
    """
    For 3-color "Pro" Launchpads with 8x8 matrix and 4x8 left/right/top/bottom rows

    LED AND BUTTON NUMBERS IN RAW MODE (DEC)
    WITH LAUNCHPAD IN "LIVE MODE" (PRESS SETUP, top-left GREEN).

    Notice that the fine manual doesn't know that mode.
    According to what's written there, the numbering used
    refers to the "PROGRAMMING MODE", which actually does
    not react to any of those notes (or numbers).

           +---+---+---+---+---+---+---+---+
           | 91|   |   |   |   |   |   | 98|
           +---+---+---+---+---+---+---+---+

    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 80|  | 81|   |   |   |   |   |   |   |  | 89|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 70|  |   |   |   |   |   |   |   |   |  | 79|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 60|  |   |   |   |   |   |   | 67|   |  | 69|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 50|  |   |   |   |   |   |   |   |   |  | 59|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 40|  |   |   |   |   |   |   |   |   |  | 49|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 30|  |   |   |   |   |   |   |   |   |  | 39|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 20|  |   |   | 23|   |   |   |   |   |  | 29|
    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 10|  |   |   |   |   |   |   |   |   |  | 19|
    +---+  +---+---+---+---+---+---+---+---+  +---+

           +---+---+---+---+---+---+---+---+
           |  1|  2|   |   |   |   |   |  8|
           +---+---+---+---+---+---+---+---+


    LED AND BUTTON NUMBERS IN XY CLASSIC MODE (X/Y)

      9      0   1   2   3   4   5   6   7      8
           +---+---+---+---+---+---+---+---+
           |0/0|   |2/0|   |   |   |   |   |         0
           +---+---+---+---+---+---+---+---+

    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |0/1|   |   |   |   |   |   |   |  |   |  1
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |9/2|  |   |   |   |   |   |   |   |   |  |   |  2
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |5/3|   |   |  |   |  3
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  4
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  5
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |4/6|   |   |   |  |   |  6
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  7
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |9/8|  |   |   |   |   |   |   |   |   |  |8/8|  8
    +---+  +---+---+---+---+---+---+---+---+  +---+

           +---+---+---+---+---+---+---+---+
           |   |1/9|   |   |   |   |   |   |         9
           +---+---+---+---+---+---+---+---+


    LED AND BUTTON NUMBERS IN XY PRO MODE (X/Y)

      0      1   2   3   4   5   6   7   8      9
           +---+---+---+---+---+---+---+---+
           |1/0|   |3/0|   |   |   |   |   |         0
           +---+---+---+---+---+---+---+---+

    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |1/1|   |   |   |   |   |   |   |  |   |  1
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |0/2|  |   |   |   |   |   |   |   |   |  |   |  2
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |6/3|   |   |  |   |  3
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  4
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  5
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |5/6|   |   |   |  |   |  6
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |   |  |   |   |   |   |   |   |   |   |  |   |  7
    +---+  +---+---+---+---+---+---+---+---+  +---+
    |0/8|  |   |   |   |   |   |   |   |   |  |9/8|  8
    +---+  +---+---+---+---+---+---+---+---+  +---+

           +---+---+---+---+---+---+---+---+
           |   |2/9|   |   |   |   |   |   |         9
           +---+---+---+---+---+---+---+---+
    """

    COLORS = {
        'black': 0,
        'off': 0,
        'white': 3,
        'red': 5,
        'green': 17,
    }

    def Open(self, number=0, name="Pro"):
        """
        Opens one of the attached Launchpad MIDI devices.
        Uses search string "Pro", by default.
        """
        retval = super(LaunchpadPro, self).Open(number=number, name=name)
        if retval:
            # avoid sending this to an Mk2
            if name.lower() == "pro":
                self.LedSetMode(0)

        return retval

    def Check(self, number=0, name="Launchpad Pro"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "Launchpad Pro", by default.
        """

        return super(LaunchpadPro, self).Check(number=number, name=name)

    # TODO: ASkr, Undocumented!
    # TODO: return value
    def LedSetLayout(self, mode) -> None:
        """
        Sets the button layout (and codes) to the set, specified by <mode>.
        Valid options:
         00 - Session, 01 - Drum Rack, 02 - Chromatic Note, 03 - User (Drum)
         04 - Audio, 05 -Fader, 06 - Record Arm, 07 - Track Select, 08 - Mute
         09 - Solo, 0A - Volume
        Until now, we'll need the "Session" (0x00) settings.
        """

        if mode < 0 or mode > 0x0d:
            return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 34, mode])
        time.wait(10)

    def LedSetMode(self, mode):
        """
        Selects the Pro's mode.
        <mode> -> 0 -> "Ableton Live mode"  (what we need)
                  1 -> "Standalone mode"    (power up default)
        """

        if mode < 0 or mode > 1:
            return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 33, mode])
        time.wait(10)

    def LedCtrlBpm(self, bpm):
        """
        Sets BPM for pulsing or flashing LEDs
        EXPERIMENTAL FAKE SHOW
        The Launchpad Pro (and Mk2) derive the LED's pulsing or flashing frequency from
        the repetive occurrence of MIDI beat clock messages (msg 248), 24 per beat.
        No timers/events here yet, so we fake it by sending the minimal amount of
        messages (25 for Pro, 26 for Mk2 (not kidding) => 28, probably safe value) once.
        The Pro and the Mk2 support 40..240 BPM, so the maximum time we block everything
        is, for 40 BPM:
          [ 1 / ( 40 BPM * 24 / 60s ) ] * 28 = 1.75s    ; (acrually one less, 28-1)
        Due to the 1ms restriction, the BPMs get quite coarse towards the faster end:
          250, 227, 208, 192, 178, 166, 156, 147, 138, 131...
        """

        bpm = min(int(bpm), 240)  # limit to upper 240
        bpm = max(bpm, 40)  # limit to lower 40

        # basically int( 1000 / ( bpm * 24 / 60.0 ) ):
        td = int(2500 / bpm)

        for _ in range(28):
            self.midi.RawWrite(248, 0, 0)
            time.wait(td)

    def LedGetColorByName(self, name):
        """
        Returns an RGB colorcode by trying to find a color of a name given by string <name>.
        If nothing was found, Code 'black' (off) is returned.
        """

        # should not be required
        # if type( name ) is not str:
        #	return 0;
        if name in LaunchpadPro.COLORS:
            return LaunchpadPro.COLORS[name]
        else:
            return LaunchpadPro.COLORS['black']

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

        if number < 0 or number > 99:
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

        if number < 0 or number > 99:
            return

        # TODO: limit/check colorcode
        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']

        self.midi.RawWrite(144, number, colorcode)

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

        # for Mk2: [ 0, 32, 41, 2, *24*, 40, *0*, number, colorcode ] (also an error in the docs)
        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 40, number, colorcode])

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

        # for Mk2: [ 0, 32, 41, 2, *24*, *35*, *0*, number, colorcode ] (also an error in the docs)
        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 35, number, colorcode])

    def LedCtrlXY(self, x, y, red, green, blue=None, mode="classic"):
        """
        Controls a grid LED by its coordinates <x>, <y> and <reg>, <green> and <blue>
        intensity values. By default, the old and compatible "Classic" mode is used
        (8x8 matrix left has x=0). If <mode> is set to "pro", x=0 will light up the round
        buttons on the left of the Launchpad Pro (not available on other models).
        This method internally uses "LedCtrlRaw()". Please also notice the comments
        in that one.
        """

        if x < 0 or x > 9 or y < 0 or y > 9:
            return

        # rotate matrix to the right, column 9 overflows from right to left, same row
        if mode != "pro":
            x = (x + 1) % 10

        # swap y
        led = 90 - (10 * y) + x

        self.LedCtrlRaw(led, red, green, blue)

    def LedCtrlXYByCode(self, x, y, colorcode, mode="classic"):
        """
        Controls a grid LED by its coordinates <x>, <y> and its <colorcode>.
        By default, the old and compatible "Classic" mode is used (8x8 matrix left has x=0).
        If <mode> is set to "pro", x=0 will light up the round buttons on the left of the
        Launchpad Pro (not available on other models).
        About three times faster than the SysEx RGB method LedCtrlXY().
        """

        if x < 0 or x > 9 or y < 0 or y > 9:
            return

        # rotate matrix to the right, column 9 overflows from right to left, same row
        if mode != "pro":
            x = (x + 1) % 10

        # swap y
        led = 90 - (10 * y) + x

        self.LedCtrlRawByCode(led, colorcode)

    def LedCtrlPulseXYByCode(self, x, y, colorcode, mode="classic"):
        """
        Pulses a grid LED by its coordinates <x>, <y> and its <colorcode>.
        By default, the old and compatible "Classic" mode is used (8x8 matrix left has x=0).
        If <mode> is set to "pro", x=0 will light up the round buttons on the left of the
        Launchpad Pro (not available on other models).
        """

        if x < 0 or x > 9 or y < 0 or y > 9:
            return

        # rotate matrix to the right, column 9 overflows from right to left, same row
        if mode != "pro":
            x = (x + 1) % 10

        # swap y
        led = 90 - (10 * y) + x

        self.LedCtrlPulseByCode(led, colorcode)

    def LedCtrlFlashXYByCode(self, x, y, colorcode, mode="classic"):
        """
        Flashes a grid LED by its coordinates <x>, <y> and its <colorcode>.
        By default, the old and compatible "Classic" mode is used (8x8 matrix left has x=0).
        If <mode> is set to "pro", x=0 will light up the round buttons on the left of the
        Launchpad Pro (not available on other models).
        """

        if x < 0 or x > 9 or y < 0 or y > 9:
            return

        # rotate matrix to the right, column 9 overflows from right to left, same row
        if mode != "pro":
            x = (x + 1) % 10

        # swap y
        led = 90 - (10 * y) + x

        self.LedCtrlFlashByCode(led, colorcode)

    def LedCtrlXYByRGB(self, x, y, lstColor, mode="classic"):
        """
        New approach to color arguments.
        Controls a grid LED by its coordinates <x>, <y> and a list of colors <lstColor>.
        <lstColor> is a list of length 3, with RGB color information, [<r>,<g>,<b>]
        """

        if type(lstColor) is not list or len(lstColor) < 3:
            return

        if x < 0 or x > 9 or y < 0 or y > 9:
            return

        # rotate matrix to the right, column 9 overflows from right to left, same row
        if mode.lower() != "pro":
            x = (x + 1) % 10

        # swap y
        led = 90 - (10 * y) + x

        self.LedCtrlRaw(led, lstColor[0], lstColor[1], lstColor[2])

    def LedCtrlChar(self, char, red, green, blue=None, offsx=0, offsy=0):
        """
        Sends character <char> in colors <red/green/blue> and lateral offset <offsx> (-8..8)
        to the Launchpad. <offsy> does not have yet any function.
        If <blue> is omitted, this method runs in "Classic" compatibility mode and the
        old 0..3 <red/green> values are multiplied with 21, to match the "Pro" 0..63 range.
        """

        char = ord(char)
        char = min(char, 255)
        char = max(char, 0) * 8

        # compatibility mode
        if blue is None:
            red *= 21
            green *= 21
            blue = 0

        for i in range(81, 1, -10):
            for j in range(8):
                sum = i + j + offsx
                if sum >= i and sum < i + 8:
                    if CHARTAB[char] & 0x80 >> j:
                        self.LedCtrlRaw(sum, red, green, blue)
                    else:
                        self.LedCtrlRaw(sum, 0, 0, 0)
            char += 1

    def LedCtrlString(self, text, red, green, blue=None, direction=None, waitms=150):
        """
        Scroll <text>, with color specified by <red/green/blue>, as fast as we can.
        <direction> specifies: -1 to left, 0 no scroll, 1 to right
        If <blue> is omitted, "Classic" compatibility mode is turned on and the old
        0..3 color intensity range is streched by 21 to 0..63.

        NEW   12/2016: More than one char on display \o/
        IDEA: variable spacing for seamless scrolling, e.g.: "__/\_"
        TODO: That <blue> compatibility thing sucks... Should be removed.
        """

        # compatibility mode
        if blue is None:
            red *= 21
            green *= 21
            blue = 0

        limit = lambda n, mini, maxi: max(min(maxi, n), mini)

        if direction == self.SCROLL_LEFT:
            text += " "  # just to avoid artifacts on full width characters
            for n in range((len(text) + 1) * 8):
                if n <= len(text) * 8:
                    self.LedCtrlChar(text[limit((n // 16) * 2, 0, len(text) - 1)], red, green, blue, 8 - n % 16)
                if n > 7:
                    self.LedCtrlChar(text[limit((((n - 8) // 16) * 2) + 1, 0, len(text) - 1)], red, green, blue,
                                     8 - (n - 8) % 16)
                time.wait(waitms)
        elif direction == self.SCROLL_RIGHT:
            # TODO: Just a quick hack (screen is erased before scrolling begins).
            #       Characters at odd positions from the right (1, 3, 5), with pixels at the left,
            #       e.g. 'C' will have artifacts at the left (pixel repeated).
            text = " " + text + " "  # just to avoid artifacts on full width characters
            #			for n in range( (len(text) + 1) * 8 - 1, 0, -1 ):
            for n in range((len(text) + 1) * 8 - 7, 0, -1):
                if n <= len(text) * 8:
                    self.LedCtrlChar(text[limit((n // 16) * 2, 0, len(text) - 1)], red, green, blue, 8 - n % 16)
                if n > 7:
                    self.LedCtrlChar(text[limit((((n - 8) // 16) * 2) + 1, 0, len(text) - 1)], red, green, blue,
                                     8 - (n - 8) % 16)
                time.wait(waitms)
        else:
            for i in text:
                for n in range(4):  # pseudo repetitions to compensate the timing a bit
                    self.LedCtrlChar(i, red, green, blue)
                    time.wait(waitms)

    def LedAllOn(self, colorcode=None):
        """
        Quickly sets all all LEDs to the same color, given by <colorcode>.
        If <colorcode> is omitted, "white" is used.
        """

        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']
        else:
            colorcode = min(colorcode, 127)
            colorcode = max(colorcode, 0)

        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 14, colorcode])

    def Reset(self):
        """
        (fake to) reset the Launchpad
        Turns off all LEDs
        """

        self.LedAllOn(0)

    def ButtonStateRaw(self, returnPressure=False):
        """
        Returns the raw value of the last button change (pressed/unpressed) as a list
        [ <button>, <value> ], in which <button> is the raw number of the button and
        <value> an intensity value from 0..127.
        >0 = button pressed; 0 = button released
        Notice that this is not (directly) compatible with the original ButtonStateRaw()
        method in the "Classic" Launchpad, which only returned [ <button>, <True/False> ].
        Compatibility would require checking via "== True" and not "is True".
        Pressure events are returned if enabled via "returnPressure".
        To distinguish pressure events from buttons, a fake button code of "255" is used,
        so the list looks like [ 255, <value> ].
        """

        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            # Note:
            #  Beside "144" (Note On, grid buttons), "208" (Pressure Value, grid buttons) and
            #  "176" (Control Change, outer buttons), random (broken) SysEx messages
            #  can appear here:
            #   ('###', [[[240, 0, 32, 41], 4]])
            #   ('-->', [])
            #   ('###', [[[2, 16, 45, 0], 4]])
            #   ('###', [[[247, 0, 0, 0], 4]])
            #  ---
            #   ('###', [[[240, 0, 32, 41], 4]])
            #   ('-->', [])
            #  1st one is a SysEx Message (240, 0, 32, 41, 2, 16 ), with command Mode Status (45)
            #  in "Ableton Mode" (0) [would be 1 for Standalone Mode). "247" is the SysEx termination.
            #  Additionally, it's interrupted by a read failure.
            #  The 2nd one is simply cut. Notice that that these are commands usually send TO the
            #  Launchpad...
            #
            # Reminder for the "pressure event issue":
            # The pressure events do not send any button codes, it's really just the pressure,
            # everytime a value changes:
            #   [[[144, 55, 5, 0], 654185]]    button hit ("NoteOn with vel > 0")
            #   [[[208, 24, 0, 0], 654275]]    button hold
            #   [[[208, 127, 0, 0], 654390]]    ...
            #   [[[208, 122, 0, 0], 654506]     ...
            #   [[[208, 65, 0, 0], 654562]]     ...
            #   [[[208, 40, 0, 0], 654567]]     ...
            #   [[[208, 0, 0, 0], 654573]]      ...
            #   [[[144, 55, 0, 0], 654614]]    button released ("NoteOn with vel == 0")
            # When multiple buttons are pressed (hold), the biggest number will be returned.
            #
            # Copied over from the XY method.
            # Try to avoid getting flooded with pressure events
            if returnPressure == False:
                while a[0][0][0] == 208:
                    a = self.midi.ReadRaw()
                    if a == []:
                        return []

            if a[0][0][0] == 144 or a[0][0][0] == 176:
                return [a[0][0][1], a[0][0][2]]
            else:
                if returnPressure:
                    if a[0][0][0] == 208:
                        return [255, a[0][0][1]]
                    else:
                        return []
                else:
                    return []
        else:
            return []

    def ButtonStateXY(self, mode="classic", returnPressure=False):
        """
        Returns the raw value of the last button change (pressed/unpressed) as a list
        [ <x>, <y>, <value> ], in which <x> and <y> are the buttons coordinates and
        <value> is the intensity from 0..127.
        >0 = button pressed; 0 = button released
        Notice that this is not (directly) compatible with the original ButtonStateRaw()
        method in the "Classic" Launchpad, which only returned [ <button>, <True/False> ].
        Compatibility would require checking via "== True" and not "is True".
        """
        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            if returnPressure == False:
                while a[0][0][0] == 208:
                    a = self.midi.ReadRaw()
                    if a == []:
                        return []

            if a[0][0][0] == 144 or a[0][0][0] == 176:

                if mode.lower() != "pro":
                    x = (a[0][0][1] - 1) % 10
                else:
                    x = a[0][0][1] % 10
                y = (99 - a[0][0][1]) // 10

                return [x, y, a[0][0][2]]
            else:
                if a[0][0][0] == 208:
                    return [255, 255, a[0][0][1]]
                else:
                    return []
        else:
            return []
