from pygame import time

from launchpad_py.charset import CHARTAB
from launchpad_py.launchpad_base import LaunchpadBase

__all__ = ['Launchpad']


class Launchpad(LaunchpadBase):
    """
    For 2-color Launchpads with 8x8 matrix and 2x8 top/right rows

    LED AND BUTTON NUMBERS IN RAW MODE (DEC):

    +---+---+---+---+---+---+---+---+
    |200|201|202|203|204|205|206|207| < AUTOMAP BUTTON CODES;
    +---+---+---+---+---+---+---+---+   Or use LedCtrlAutomap() for LEDs (alt. args)

    +---+---+---+---+---+---+---+---+  +---+
    |  0|...|   |   |   |   |   |  7|  |  8|
    +---+---+---+---+---+---+---+---+  +---+
    | 16|...|   |   |   |   |   | 23|  | 24|
    +---+---+---+---+---+---+---+---+  +---+
    | 32|...|   |   |   |   |   | 39|  | 40|
    +---+---+---+---+---+---+---+---+  +---+
    | 48|...|   |   |   |   |   | 55|  | 56|
    +---+---+---+---+---+---+---+---+  +---+
    | 64|...|   |   |   |   |   | 71|  | 72|
    +---+---+---+---+---+---+---+---+  +---+
    | 80|...|   |   |   |   |   | 87|  | 88|
    +---+---+---+---+---+---+---+---+  +---+
    | 96|...|   |   |   |   |   |103|  |104|
    +---+---+---+---+---+---+---+---+  +---+
    |112|...|   |   |   |   |   |119|  |120|
    +---+---+---+---+---+---+---+---+  +---+


    LED AND BUTTON NUMBERS IN XY MODE (X/Y)

      0   1   2   3   4   5   6   7      8
    +---+---+---+---+---+---+---+---+
    |   |1/0|   |   |   |   |   |   |         0
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

    def Reset(self) -> None:
        """
        reset the Launchpad
        Turns off all LEDs
        """
        self.midi.RawWrite(176, 0, 0)

    def LedGetColor(self, red, green):
        """
        Returns a Launchpad compatible "color code byte"
        NOTE: In here, number is 0..7 (left..right)
        """

        led = 0

        red = min(int(red), 3)  # make int and limit to <=3
        red = max(red, 0)  # no negative numbers

        green = min(int(green), 3)  # make int and limit to <=3
        green = max(green, 0)  # no negative numbers

        led |= red
        led |= green << 4

        return led

    def LedCtrlRaw(self, number, red, green):
        """
        Controls a grid LED by its raw <number>; with <green/red> brightness: 0..3
        For LED numbers, see grid description on top of class.
        """

        if number > 199:
            if number < 208:
                # 200-207
                self.LedCtrlAutomap(number - 200, red, green)
        else:
            if number < 0 or number > 120:
                return
            # 0-120
            led = self.LedGetColor(red, green)
            self.midi.RawWrite(144, number, led)

    def LedCtrlXY(self, x, y, red, green):
        """
        Controls a grid LED by its coordinates <x> and <y>  with <green/red> brightness 0..3
        """

        if x < 0 or x > 8 or y < 0 or y > 8:
            return

        if y == 0:
            self.LedCtrlAutomap(x, red, green)

        else:
            self.LedCtrlRaw(((y - 1) << 4) | x, red, green)

    def LedCtrlRawRapid(self, allLeds):
        """
        Sends a list of consecutive, special color values to the Launchpad.
        Only requires (less than) half of the commands to update all buttons.
        [ LED1, LED2, LED3, ... LED80 ]
        First, the 8x8 matrix is updated, left to right, top to bottom.
        Afterward, the algorithm continues with the rightmost buttons and the
        top "automap" buttons.
        LEDn color format: 00gg00rr <- 2 bits green, 2 bits red (0..3)
        Function LedGetColor() will do the coding for you...
        Notice that the amount of LEDs needs to be even.
        If an odd number of values is sent, the next, following LED is turned off!
        REFAC2015: Device specific.
        """
        le = len(allLeds)

        for i in range(0, le, 2):
            self.midi.RawWrite(146, allLeds[i], allLeds[i + 1] if i + 1 < le else 0)

        #   This fast version does not work, because the Launchpad gets confused
        #   by the timestamps...
        #
        #		tmsg= []
        #		for i in range( 0, le, 2 ):
        #			# create a message
        #			msg = [ 146 ]
        #			msg.append( allLeds[i] )
        #			if i+1 < le:
        #				msg.append( allLeds[i+1] )
        #			# add it to the list
        #			tmsg.append( msg )
        #			# add a timestanp
        #			tmsg.append( self.midi.GetTime() + i*10 )
        #
        #		self.midi.RawWriteMulti( [ tmsg ] )

    def LedCtrlRawRapidHome(self) -> None:
        """
        "Homes" the next LedCtrlRawRapid() call, so it will start with the first LED again.
        """
        self.midi.RawWrite(176, 1, 0)

    def LedCtrlAutomap(self, number, red, green):
        """
        Controls an automap LED <number>; with <green/red> brightness: 0..3
        NOTE: In here, number is 0..7 (left..right)
        """

        if number < 0 or number > 7:
            return

        red = max(0, red)
        red = min(3, red)
        green = max(0, green)
        green = min(3, green)
        led = self.LedGetColor(red, green)

        self.midi.RawWrite(176, 104 + number, led)

    def LedAllOn(self, colorcode=None):
        """
        all LEDs on
        <colorcode> is here for backwards compatibility with the newer "Mk2" and "Pro"
        classes. If it's "0", all LEDs are turned off. In all other cases turned on,
        like the function name implies :-/
        """
        if colorcode == 0:
            self.Reset()
        else:
            self.midi.RawWrite(176, 0, 127)

    def LedCtrlChar(self, char, red, green, offsx=0, offsy=0):
        """
        Sends character <char> in colors <red/green> and lateral offset <offsx> (-8..8)
        to the Launchpad. <offsy> does not have yet any function
        """
        char = ord(char)

        if char < 0 or char > 255:
            return
        char *= 8

        for i in range(0, 8 * 16, 16):
            for j in range(8):
                lednum = i + j + offsx
                if lednum >= i and lednum < i + 8:
                    if CHARTAB[char] & 0x80 >> j:
                        self.LedCtrlRaw(lednum, red, green)
                    else:
                        self.LedCtrlRaw(lednum, 0, 0)
            char += 1

    def LedCtrlString(self, text, red, green, direction=None, waitms=150):
        """
        Scroll <text>, in colors specified by <red/green>, as fast as we can.
        <direction> specifies: -1 to left, 0 no scroll, 1 to right
        The delays were a dirty hack, but there's little to nothing one can do here.
        So that's how the <waitms> parameter came into play...
        NEW   12/2016: More than one char on display \o/
        IDEA: variable spacing for seamless scrolling, e.g.: "__/\_"
        """

        limit = lambda n, mini, maxi: max(min(maxi, n), mini)

        if direction == self.SCROLL_LEFT:
            text += " "
            for n in range((len(text) + 1) * 8):
                if n <= len(text) * 8:
                    self.LedCtrlChar(text[limit((n // 16) * 2, 0, len(text) - 1)], red, green, 8 - n % 16)
                if n > 7:
                    self.LedCtrlChar(text[limit((((n - 8) // 16) * 2) + 1, 0, len(text) - 1)], red, green,
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
                    self.LedCtrlChar(text[limit((n // 16) * 2, 0, len(text) - 1)], red, green, 8 - n % 16)
                if n > 7:
                    self.LedCtrlChar(text[limit((((n - 8) // 16) * 2) + 1, 0, len(text) - 1)], red, green,
                                     8 - (n - 8) % 16)
                time.wait(waitms)
        else:
            for i in text:
                for n in range(4):  # pseudo repetitions to compensate the timing a bit
                    self.LedCtrlChar(i, red, green)
                    time.wait(waitms)

    def ButtonChanged(self):
        """
        Returns True if a button event was received.
        """
        return self.midi.ReadCheck()

    def ButtonStateRaw(self):
        """
        Returns the raw value of the last button change as a list:
        [ <button>, <True/False> ]
        """

        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()
            return [a[0][0][1] if a[0][0][0] == 144 else a[0][0][1] + 96, True if a[0][0][2] > 0 else False]
        else:
            return []

    def ButtonStateXY(self):
        """
        Returns an x/y value of the last button change as a list:
        [ <x>, <y>, <True/False> ]
        """
        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            if a[0][0][0] == 144:
                x = a[0][0][1] & 0x0f
                y = (a[0][0][1] & 0xf0) >> 4

                return [x, y + 1, True if a[0][0][2] > 0 else False]

            elif a[0][0][0] == 176:
                return [a[0][0][1] - 104, 0, True if a[0][0][2] > 0 else False]

        return []
