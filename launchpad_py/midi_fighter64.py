from pygame import time

from launchpad_py.charset import CHARTAB
from launchpad_py.launchpad_base import LaunchpadBase

__all__ = ['MidiFighter64']


class MidiFighter64(LaunchpadBase):
    """
    For Midi Fighter 64 Gedöns

    LED AND BUTTON NUMBERS IN RAW MODE

           +---+---+---+---+---+---+---+---+
           | 64|   |   | 67| 96|   |   | 99|
           +---+---+---+---+---+---+---+---+
           | 60|   |   | 63| 92|   |   | 95|
           +---+---+---+---+---+---+---+---+
           | 56|   |   | 59| 88|   |   | 91|
           +---+---+---+---+---+---+---+---+
           | 52|   |   | 55| 84|   |   | 87|
           +---+---+---+---+---+---+---+---+
           | 48|   |   | 51| 80|   |   | 83|
           +---+---+---+---+---+---+---+---+
           | 44|   |   | 47| 76|   |   | 79|
           +---+---+---+---+---+---+---+---+
           | 40|   |   | 43| 72|   |   | 75|
           +---+---+---+---+---+---+---+---+
           | 36|   |   | 39| 68|   |   | 71|
           +---+---+---+---+---+---+---+---+


    LED AND BUTTON NUMBERS IN XY MODE (X/Y)

             0   1   2   3   4   5   6   7
           +---+---+---+---+---+---+---+---+
           |0/0|   |   |   |   |   |   |   | 0
           +---+---+---+---+---+---+---+---+
           |   |   |   |   |   |   |   |   | 1
           +---+---+---+---+---+---+---+---+
           |   |   |   |   |   |5/2|   |   | 2
           +---+---+---+---+---+---+---+---+
           |   |   |   |   |   |   |   |   | 3
           +---+---+---+---+---+---+---+---+
           |   |   |   |   |   |   |   |   | 4
           +---+---+---+---+---+---+---+---+
           |   |   |   |   |4/5|   |   |   | 5
           +---+---+---+---+---+---+---+---+
           |   |   |   |   |   |   |   |   | 6
           +---+---+---+---+---+---+---+---+
           |   |   |   |   |   |   |   |   | 7
           +---+---+---+---+---+---+---+---+
    """

    def __init__(self):
        """
        Add some LED mode "constants" for better usability.
        """

        self.MODE_BRIGHT = [i + 18 for i in range(16)]
        self.MODE_TOGGLE = [i + 34 for i in range(8)]
        self.MODE_PULSE = [i + 42 for i in range(8)]
        self.MODE_ANIM_SQUARE = 50
        self.MODE_ANIM_CIRCLE = 51
        self.MODE_ANIM_STAR = 52
        self.MODE_ANIM_TRIANGLE = 53

        super(MidiFighter64, self).__init__()

    def Open(self, number=0, name="Fighter 64"):
        """
        Opens one of the attached Launchpad MIDI devices.
        Uses search string "Fighter 64", by default.
        """
        return super(MidiFighter64, self).Open(number=number, name=name)

    def Check(self, number=0, name="Fighter 64"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "Fighter 64", by default.
        """
        return super(MidiFighter64, self).Check(number=number, name=name)

    def LedCtrlRaw(self, number, color, mode=None):
        """
        Controls a grid LED by its <number> and a <color>.
         <number> 36..99
         <color>   0..127 from color table
         <mode>   18..53  for brightness, toggling and animation
        """

        if number < 36 or number > 99:
            return
        if color < 0 or color > 127:
            return

        self.midi.RawWrite(146, number, color)

        # faster than calling LedCtrlRawMode()
        if mode is not None and mode > 17 and mode < 54:
            self.midi.RawWrite(147, number - 3 * 12, mode)

    def LedCtrlRawMode(self, number, mode):
        """
        Controls a the mode of a grid LED by its <number> and the mode <mode> of the LED.
         <number> 36..99
         <mode>   18..53 for brightness, toggling and animation
        Internal LED numbers are 3 octaves lower than the color numbers.
        The mode must be sent over channel 4
        """

        # uses the original button numbers for usability
        if number < 36 or number > 99:
            return
        if mode < 18 or mode > 53:
            return

        self.midi.RawWrite(147, number - 3 * 12, mode)

    def LedCtrlXY(self, x, y, color, mode=None):
        """
        Controls a grid LED by its <x>/<y> coordinates and a <color>.
         <x>/<y>  0..7
         <color>  0..127 from color table
        """

        if x < 0 or x > 7:
            return
        if y < 0 or y > 7:
            return
        if color < 0 or color > 127:
            return

        if x < 4:
            number = 36 + x % 4
        else:
            number = 68 + x % 4

        number += (7 - y) * 4

        self.midi.RawWrite(146, number, color)
        # set the mode if required; faster than calling LedCtrlRawMode()
        if mode is not None and mode > 17 and mode < 54:
            self.midi.RawWrite(147, number - 3 * 12, mode)

    def LedCtrlChar(self, char, colorcode, offsx=0, offsy=0, coloroff=0):
        """
        Displays the character <char> with color of <colorcode> and lateral offset
        <offsx> (-8..8) on the Midi Fighter. <offsy> does not have yet any function.
        <coloroff> specifies the background color.
        Notice that the call to this method is not compatible to the Launchpad variants,
        because the Midi Fighter lacks support for RGB.
        """

        char = ord(char)
        char = min(char, 255)
        char = max(char, 0) * 8

        if colorcode < 0 or colorcode > 127:
            return

        for y in range(64, 35, -4):
            for x in range(8):
                number = y + x + offsx
                if x + offsx > 3:
                    number += 28  # +32-4

                if x + offsx < 8 and x + offsx >= 0:
                    if CHARTAB[char] & 0x80 >> x:
                        self.LedCtrlRaw(number, colorcode)
                    else:
                        # lol, shit; there is no color code for "off"
                        self.LedCtrlRaw(number, coloroff)
            char += 1

    def LedCtrlString(self, text, colorcode, coloroff=0, direction=None, waitms=150):
        """
        Scroll <text>, with color specified by <colorcode>, as fast as we can.
        <direction> specifies: -1 to left, 0 no scroll, 1 to right
        Notice that the call to this method is not compatible to the Launchpad variants,
        because the Midi Fighter lacks support for RGB.
        """

        limit = lambda n, mini, maxi: max(min(maxi, n), mini)

        if direction == self.SCROLL_LEFT:
            text += " "  # just to avoid artifacts on full width characters
            for n in range((len(text) + 1) * 8):
                if n <= len(text) * 8:
                    self.LedCtrlChar(text[limit((n // 16) * 2, 0, len(text) - 1)], colorcode, 8 - n % 16,
                                     coloroff=coloroff)
                if n > 7:
                    self.LedCtrlChar(text[limit((((n - 8) // 16) * 2) + 1, 0, len(text) - 1)], colorcode,
                                     8 - (n - 8) % 16, coloroff=coloroff)
                time.wait(waitms)
        elif direction == self.SCROLL_RIGHT:
            # TODO: Just a quick hack (screen is erased before scrolling begins).
            #       Characters at odd positions from the right (1, 3, 5), with pixels at the left,
            #       e.g. 'C' will have artifacts at the left (pixel repeated).
            text = " " + text + " "  # just to avoid artifacts on full width characters
            #			for n in range( (len(text) + 1) * 8 - 1, 0, -1 ):
            for n in range((len(text) + 1) * 8 - 7, 0, -1):
                if n <= len(text) * 8:
                    self.LedCtrlChar(text[limit((n // 16) * 2, 0, len(text) - 1)], colorcode, 8 - n % 16,
                                     coloroff=coloroff)
                if n > 7:
                    self.LedCtrlChar(text[limit((((n - 8) // 16) * 2) + 1, 0, len(text) - 1)], colorcode,
                                     8 - (n - 8) % 16, coloroff=coloroff)
                time.wait(waitms)
        else:
            for i in text:
                for n in range(4):  # pseudo repetitions to compensate the timing a bit
                    self.LedCtrlChar(i, colorcode, coloroff=coloroff)
                    time.wait(waitms)

    def LedAllOn(self, color=3, mode=None):
        """
        Sets all LEDs to the same color, specified by <color>.
        If color is omitted, the LEDs are set to white (code 3)
        """

        for i in range(64):
            self.LedCtrlRaw(i + 36, color, mode)

    def ButtonStateRaw(self):
        """
        Returns the raw value of the last button change (pressed/unpressed) as a list
        [ <button>, <velocity> ], in which <button> is the raw number of the button and
        <velocity> the button state.
          >0 = button pressed; 0 = button released
        """

        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            # The Midi Fighter 64 does not support velocities. For 500 bucks. Lol :'-)
            # What we see here are either channel 3 or 2 NoteOn/NoteOff commands,
            # the factory settings, depending on the "bank selection".
            #   Channel 3 -> hold upper left  button for longer than 2s
            #   Channel 2 -> hold upper right button for longer than 2s
            #
            #    [[[146, 81, 127, 0], 47365]]
            #    [[[130, 81, 127, 0], 47443]]
            #    [[[146, 82, 127, 0], 47610]]
            #
            #    [[[ <NoteOn/Off>, <button>, 127, 0], 47610]]
            #
            #    146/145 -> NoteOn
            #    130/129 -> NoteOff
            #    127     -> fixed velocity (as set by the Midi Fighter utility )

            # Mhh, I guess it's about time to think about adding MIDI channels, isn't it?
            # But for now, we just check ch 2 and 3:
            if a[0][0][0] == 145 or a[0][0][0] == 146:
                return [a[0][0][1], a[0][0][2]]
            else:
                if a[0][0][0] == 130 or a[0][0][0] == 129:
                    return [a[0][0][1], 0]
                else:
                    return []
        else:
            return []

    def ButtonStateXY(self):
        """
        Returns the raw value of the last button change (pressed/unpressed) as a list
        [ <x>, <y>, <velocity> ], in which <x>/<y> are the coordinates of the grid and
        <velocity> the state of the button.
          >0 = button pressed; 0 = button released
        """

        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            # whatever that is, does not belong here...
            if a[0][0][1] < 36 or a[0][0][1] > 99:
                return []

            x = (a[0][0][1] - 36) % 4
            if a[0][0][1] >= 68:
                x += 4
            y = 7 - ((a[0][0][1] - 36) % 32) // 4

            if a[0][0][0] == 145 or a[0][0][0] == 146:
                return [x, y, a[0][0][2]]
            else:
                if a[0][0][0] == 130 or a[0][0][0] == 129:
                    return [x, y, 0]
                else:
                    return []
        else:
            return []

    def Reset(self):
        """
        Reset the Midi Fighter
        Well, at least turn off all its LEDs
        """
        # TODO
        # self.LedAllOn( 0 )
        pass
