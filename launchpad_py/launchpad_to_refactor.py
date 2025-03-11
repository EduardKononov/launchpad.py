import sys

from pygame import time

from launchpad_py import LaunchpadPro
from launchpad_py.launchpad_base import LaunchpadBase

try:
    from launchpad_py.charset import *
except ImportError:
    try:
        from charset import *
    except ImportError:
        sys.exit("error loading Launchpad charset")


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

    """
    # --
    # --
    """

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


########################################################################################
### CLASS LaunchControlXL
###
########################################################################################
class LaunchControlXL(LaunchpadBase):
    """
    For 2-color Launch Control XL

    LED, BUTTON AND POTENTIOMETER NUMBERS IN RAW MODE (DEC)

        +---+---+---+---+---+---+---+---+  +---++---+
        | 13| 29| 45| 61| 77| 93|109|125|  |NOP||NOP|
        +---+---+---+---+---+---+---+---+  +---++---+
        | 14| 30| 46| 62| 78| 94|110|126|  |104||105|
        +---+---+---+---+---+---+---+---+  +---++---+
        | 15| 31| 47| 63| 79| 95|111|127|  |106||107|
        +---+---+---+---+---+---+---+---+  +---++---+

        +---+---+---+---+---+---+---+---+     +---+
        |   |   |   |   |   |   |   |   |     |105|
        |   |   |   |   |   |   |   |   |     +---+
        |   |   |   |   |   |   |   |   |     |106|
        | 77| 78| 79| 80| 81| 82| 83| 84|     +---+
        |   |   |   |   |   |   |   |   |     |107|
        |   |   |   |   |   |   |   |   |     +---+
        |   |   |   |   |   |   |   |   |     |108|
        +---+---+---+---+---+---+---+---+     +---+

        +---+---+---+---+---+---+---+---+
        | 41| 42| 43| 44| 57| 58| 59| 60|
        +---+---+---+---+---+---+---+---+
        | 73| 74| 75| 76| 89| 90| 91| 92|
        +---+---+---+---+---+---+---+---+


    LED NUMBERS IN X/Y MODE (DEC)

          0   1   2   3   4   5   6   7      8    9

        +---+---+---+---+---+---+---+---+  +---++---+
     0  |0/1|   |   |   |   |   |   |   |  |NOP||NOP|  0
        +---+---+---+---+---+---+---+---+  +---++---+
     1  |   |   |   |   |   |   |   |   |  |   ||   |  1
        +---+---+---+---+---+---+---+---+  +---++---+
     2  |   |   |   |   |   |5/2|   |   |  |   ||   |  2
        +---+---+---+---+---+---+---+---+  +---++---+
                                               8/9
        +---+---+---+---+---+---+---+---+     +---+
        |   |   |   |   |   |   |   |   |     |   |    3(!)
        |   |   |   |   |   |   |   |   |     +---+
        |   |   |   |   |   |   |   |   |     |   |    4(!)
     3  |   |   |2/3|   |   |   |   |   |     +---+
        |   |   |   |   |   |   |   |   |     |   |    5(!)
        |   |   |   |   |   |   |   |   |     +---+
        |   |   |   |   |   |   |   |   |     |   |    6
        +---+---+---+---+---+---+---+---+     +---+

        +---+---+---+---+---+---+---+---+
     4  |   |   |   |   |   |   |   |   |              4(!)
        +---+---+---+---+---+---+---+---+
     5  |   |   |   |3/4|   |   |   |   |              5(!)
        +---+---+---+---+---+---+---+---+
    """

    def Open(self, number=0, name="Control XL", template=1):
        """
        # -- Opens one of the attached Control XL MIDI devices.
        # -- Uses search string "Control XL", by default.
        """

        # The user template number adds to the MIDI commands.
        # Make sure that the Control XL is set to the corresponding mode by
        # holding down one of the template buttons and selecting the template
        # with the lowest button row 1..8
        # By default, user template 1 is enabled. Notice that the Launch Control
        # actually uses 0..15, but as the pad buttons are labeled 1..8 it probably
        # makes sense to use these human-readable ones instead.

        template = min(int(template), 16)  # make int and limit to <=8
        template = max(template, 1)  # no negative numbers

        self.UserTemplate = template

        retval = super(LaunchControlXL, self).Open(number=number, name=name)
        if retval == True:
            self.TemplateSet(self.UserTemplate)

        return retval

    def Check(self, number=0, name="Control XL"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "Pro", by default.
        """
        return super(LaunchControlXL, self).Check(number=number, name=name)

    def TemplateSet(self, templateNum):
        """
        Sets the layout template.
        1..8 selects the user and 9..16 the factory setups.
        """
        if templateNum < 1 or templateNum > 16:
            return
        else:
            self.UserTemplate = templateNum
            self.midi.RawWriteSysEx([0, 32, 41, 2, 17, 119, templateNum - 1])

    def Reset(self):
        """
        reset the Launchpad; only reset the current template
        Turns off all LEDs
        """
        self.midi.RawWrite(176 + self.UserTemplate - 1, 0, 0)

    def LedAllOn(self, colorcode=None):
        """
        all LEDs on
        <colorcode> is here for backwards compatibility with the newer "Mk2" and "Pro"
        classes. If it's "0", all LEDs are turned off. In all other cases turned on,
        like the function name implies :-/
        """
        if colorcode is None or colorcode == 0:
            self.Reset()
        else:
            self.midi.RawWrite(176, 0, 127)

    def LedGetColor(self, red, green):
        """
        Returns a Launchpad compatible "color code byte"
        NOTE: In here, number is 0..7 (left..right)
        """
        # TODO: copy and clear bits
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
        # the order of the LEDs is really a mess
        led = self.LedGetColor(red, green)
        self.midi.RawWrite(144, number, led)

    def LedCtrlXY(self, x, y, red, green):
        """
        Controls a grid LED by its coordinates <x> and <y>  with <green/red> brightness 0..3
        """
        # TODO: Note about the y coords
        if x < 0 or x > 9 or y < 0 or y > 6:
            return

        if x < 8:
            color = self.LedGetColor(red, green)
        else:
            # the "special buttons" only have one color
            color = self.LedGetColor(3, 3)

        # TODO: double code ahead ("37 + y"); query "y>2" first, then x...

        if x < 8:
            if y < 3:
                index = y * 8 + x
            elif y > 3 and y < 6:
                # skip row 3 and continue with 4 and 5
                index = (y - 1) * 8 + x
            else:
                return
        # -----
        elif x == 8:
            # ----- device, mute, solo, record
            if y > 2:
                index = 37 + y
            # ----- up
            elif y == 1:
                index = 44
            # ----- left
            elif y == 2:
                index = 46
            else:
                return
        # -----
        elif x == 9:
            # ----- device, mute, solo, record
            if y > 2:
                index = 37 + y
            # ----- down
            elif y == 1:
                index = 45
            # ----- right
            elif y == 2:
                index = 47
            else:
                return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 17, 120, 0, index, color])

    def InputFlush(self):
        """
        Clears the input buffer (The Launchpads remember everything...)
        """
        return self.ButtonFlush()

    def InputChanged(self):
        """
        Returns True if an event occured.
        """
        return self.midi.ReadCheck()

    def InputStateRaw(self):
        """
        Returns the raw value of the last button or potentiometer change as a list:
        potentiometers/sliders:  <pot.number>, <value>     , 0 ]
        buttons:                 <pot.number>, <True/False>, 0 ]
        """
        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            # --- pressed
            if a[0][0][0] == 144:
                return [a[0][0][1], True, 127]
            # --- released
            elif a[0][0][0] == 128:
                return [a[0][0][1], False, 0]
            # --- potentiometers and the four cursor buttons
            elif a[0][0][0] == 176:
                # --- cursor buttons
                if a[0][0][1] >= 104 and a[0][0][1] <= 107:
                    if a[0][0][2] > 0:
                        return [a[0][0][1], True, a[0][0][2]]
                    else:
                        return [a[0][0][1], False, 0]
                # --- potentiometers
                else:
                    return [a[0][0][1], a[0][0][2], 0]
            else:
                return []
        else:
            return []


########################################################################################
### CLASS LaunchControl
###
########################################################################################
class LaunchControl(LaunchControlXL):
    """
    For 2-color Launch Control

    LED, BUTTON AND POTENTIOMETER NUMBERS IN RAW MODE (DEC)

          0   1   2   3   4   5   6   7      8    9

        +---+---+---+---+---+---+---+---+  +---++---+
     0  | 21| 22| 23| 24| 25| 26| 27| 28|  |NOP||NOP|
        +---+---+---+---+---+---+---+---+  +---++---+
     1  | 41| 42| 43| 44| 45| 46| 47| 48|  |114||115|
        +---+---+---+---+---+---+---+---+  +---++---+
        +---+---+---+---+---+---+---+---+  +---++---+
     2  |  9| 10| 11| 12| 25| 26| 27| 28|  |116||117|
        +---+---+---+---+---+---+---+---+  +---++---+


    LED NUMBERS IN X/Y MODE (DEC)

          0   1   2   3   4   5   6   7      8    9

        +---+---+---+---+---+---+---+---+  +---++---+
        | - | - | - | - | - | - | - | - |  |NOP||NOP|
        +---+---+---+---+---+---+---+---+  +---++---+
     1  | - | - | - | - | - | - | - | - |  |8/1||9/1|
        +---+---+---+---+---+---+---+---+  +---++---+
        +---+---+---+---+---+---+---+---+  +---++---+
     0  |0/0|   |   |   |   |   |   |7/0|  |8/0||9/0|
        +---+---+---+---+---+---+---+---+  +---++---+
    """

    def Open(self, number=0, name="Control MIDI", template=1):
        """
        Opens one of the attached Control MIDI devices.
        Uses search string "Control MIDI", by default.
        """

        # The user template number adds to the MIDI commands.
        # Make sure that the Control is set to the corresponding mode by
        # holding down one of the template buttons and selecting the template
        # with the lowest button row 1..8 (variable here stores that as 0..7 for
        # user or 8..15 for the factory templates).
        # By default, user template 0 is enabled
        self.UserTemplate = template

        retval = super(LaunchControl, self).Open(number=number, name=name)
        if retval == True:
            self.TemplateSet(self.UserTemplate)

        return retval

    def Check(self, number=0, name="Control MIDI"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "Control MIDI", by default.
        """
        return super(LaunchControl, self).Check(number=number, name=name)

    def TemplateSet(self, templateNum):
        """
        Sets the layout template.
        1..8 selects the user and 9..16 the factory setups.
        """
        if templateNum < 1 or templateNum > 16:
            return
        else:
            self.midi.RawWriteSysEx([0, 32, 41, 2, 10, 119, templateNum - 1])

    def LedCtrlXY(self, x, y, red, green):
        """
        Controls a grid LED by its coordinates <x> and <y>  with <green/red> brightness 0..3
        Actually, this doesn't make a lot of sense as the Control only has one row
        of LEDs, but anyway ...
        """

        # TODO: Note about the y coords
        if x < 0 or x > 9 or y < 0 or y > 1:
            return

        if x < 8:
            color = self.LedGetColor(red, green)
        else:
            # the "special buttons" only have one color
            color = self.LedGetColor(3, 3)

        if y == 0:
            #			index = [ 9, 10, 11, 12, 25, 26, 27, 28, 116, 117 ][x]
            index = [0, 1, 2, 3, 4, 5, 6, 7, 10, 11][x]
        else:
            if x == 8:
                index = 8
            elif x == 9:
                index = 9
            else:
                return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 10, 120, 0, index, color])


class LaunchKeyMini(LaunchpadBase):
    """
    For 2-color LaunchKey Keyboards

    LED, BUTTON, KEY AND POTENTIOMETER NUMBERS IN RAW MODE (DEC)
    NOTICE THAT THE OCTAVE BUTTONS SHIFT THE KEYS UP OR DOWN BY 12.

    LAUNCHKEY MINI:

                      +---+---+---+---+---+---+---+---+
                      | 21| 22|...|   |   |   |   | 28|
        +---+---+---+ +---+---+---+---+---+---+---+---+ +---+  +---+
        |106|107|NOP| | 40| 41| 42| 43| 48| 49| 50| 51| |108|  |104|
        +---+---+---+ +---+---+---+---+---+---+---+---+ +---+  +---+
        |NOP|NOP|     | 36| 37| 38| 39| 44| 45| 46| 47| |109|  |105|
        +---+---+     +---+---+---+---+---+---+---+---+ +---+  +---+

        +--+-+-+-+--+--+-+-+-+-+-+--+--+-+-+-+--+--+-+-+-+-+-+--+---+
        |  | | | |  |  | | | | | |  |  | | | |  |  | | | | | |  |   |
        |  |4| |5|  |  | | | | | |  |  |6| | |  |  | | | | |7|  |   |
        |  |9| |1|  |  | | | | | |  |  |1| | |  |  | | | | |0|  |   |
        |  +-+ +-+  |  +-+ +-+ +-+  |  +-+ +-+  |  +-+ +-+ +-+  |   |
        | 48| 50| 52|   |   |   |   | 60|   |   |   |   |   | 71| 72|
        |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
        | C | D | E |...|   |   |   | C2| D2|...|   |   |   |   | C3|
        +---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+


    LAUNCHKEY 25/49/61:

       SLIDERS:           41..48
       SLIDER (MASTER):   7

    """

    def Open(self, number=0, name="LaunchKey"):
        """
        Opens one of the attached LaunchKey devices.
        Uses search string "LaunchKey", by default.
        """
        retval = super(LaunchKeyMini, self).Open(number=number, name=name)
        return retval

    def Check(self, number=0, name="LaunchKey"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "LaunchKey", by default.
        """
        return super(LaunchKeyMini, self).Check(number=number, name=name)

    def InputStateRaw(self):
        """
        Returns the raw value of the last button, key or potentiometer change as a list:
        potentiometers:   <pot.number>, <value>     , 0          ]
        buttons:          <but.number>, <True/False>, <velocity> ]
        keys:             <but.number>, <True/False>, <velocity> ]
        If a button does not provide an analog value, 0 or 127 are returned as velocity values.
        Because of the octave settings cover the complete note range, the button and potentiometer
        numbers collide with the note numbers in the lower octaves.
        """
        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            # pressed key
            if a[0][0][0] == 144:
                return [a[0][0][1], True, a[0][0][2]]
            # released key
            elif a[0][0][0] == 128:
                return [a[0][0][1], False, 0]
            # pressed button
            elif a[0][0][0] == 153:
                return [a[0][0][1], True, a[0][0][2]]
            # released button
            elif a[0][0][0] == 137:
                return [a[0][0][1], False, 0]
            # potentiometers and the four cursor buttons
            elif a[0][0][0] == 176:
                # cursor, track and scene buttons
                if a[0][0][1] >= 104 and a[0][0][1] <= 109:
                    if a[0][0][2] > 0:
                        return [a[0][0][1], True, 127]
                    else:
                        return [a[0][0][1], False, 0]
                # potentiometers
                else:
                    return [a[0][0][1], a[0][0][2], 0]
            else:
                return []
        else:
            return []

    def InputFlush(self):
        """
        Clears the input buffer (The Launchpads remember everything...)
        """
        return self.ButtonFlush()

    def InputChanged(self):
        """
        Returns True if an event occured.
        """
        return self.midi.ReadCheck()


class Dicer(LaunchpadBase):
    """
    For that Dicer thingy...

    LED, BUTTON, KEY AND POTENTIOMETER NUMBERS IN RAW MODE (DEC)
    NOTICE THAT THE OCTAVE BUTTONS SHIFT THE KEYS UP OR DOWN BY 10.

    FOR SHIFT MODE (HOLD ONE OF THE 3 MODE BUTTONS): ADD "5".
        +-----+  +-----+  +-----+             +-----+  +-----+  +-----+
        |#    |  |#    |  |     |             |#   #|  |#   #|  |    #|
        |  #  |  |     |  |  #  |             |  #  |  |     |  |  #  |
        |    #|  |    #|  |     |             |#   #|  |#   #|  |#    |
        +-----+  +-----+  +-----+             +-----+  +-----+  +-----+

        +-----+            +---+               +----+           +-----+
        |#   #|            | +0|               |+120|           |    #|
        |     |            +---+               +----+           |     |
        |#   #|       +---+                         +----+      |#    |
        +-----+       |+10|                         |+110|      +-----+
                      +---+                         +----+
        +-----+  +---+                                  +----+  +-----+
        |#   #|  |+20|                                  |+100|  |     |
        |  #  |  +---+                                  +----+  |  #  |
        |#   #|                                                 |     |
        +-----+                                                 +-----+


    """

    def Open(self, number=0, name="Dicer"):
        """
        Opens one of the attached Dicer devices.
        Uses search string "dicer", by default.
        """
        retval = super(Dicer, self).Open(number=number, name=name)
        return retval

    def Check(self, number=0, name="Dicer"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "dicer", by default.
        """
        return super(Dicer, self).Check(number=number, name=name)

    def Reset(self):
        """
        reset the Dicer
        Turns off all LEDs, restores power-on state, but does not disable an active light show.
        """
        self.midi.RawWrite(186, 0, 0)

    def LedAllOff(self):
        """
        Turns off all LEDs, does not change or touch any other settings.
        """
        self.midi.RawWrite(186, 0, 112)

    def ButtonStateRaw(self):
        """
        Returns (an already nicely mapped and not raw :) value of the last button change as a list:
        buttons: <number>, <True/False>, <velocity> ]
        If a button does not provide an analog value, 0 or 127 are returned as velocity values.
        Small buttons select either 154, 155, 156 cmd for master or 157, 158, 159 for slave.
        Button numbers (1 to 5): 60, 61 .. 64; always
        Guess it's best to return: 1..5, 11..15, 21..25 for Master and 101..105, ... etc for slave
        Actually, as you can see, it's not "raw", but I guess those decade modifiers really
        make sense here (less brain calculations for you :)
        """
        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            # button on master
            if a[0][0][0] >= 154 and a[0][0][0] <= 156:
                butNum = a[0][0][1]
                if butNum >= 60 and butNum <= 69:
                    butNum -= 59
                    butNum += 10 * (a[0][0][0] - 154)
                    if a[0][0][2] == 127:
                        return [butNum, True, 127]
                    else:
                        return [butNum, False, 0]
                else:
                    return []
            # button on master
            elif a[0][0][0] >= 157 and a[0][0][0] <= 159:
                butNum = a[0][0][1]
                if butNum >= 60 and butNum <= 69:
                    butNum -= 59
                    butNum += 100 + 10 * (a[0][0][0] - 157)
                    if a[0][0][2] == 127:
                        return [butNum, True, 127]
                    else:
                        return [butNum, False, 0]
                else:
                    return []
        else:
            return []

    def LedSetLightshow(self, device, enable):
        """
        Enables or disables the Dicer's built-in light show.
        Device: 0 = Master, 1 = Slave; enable = True/False
        """
        # Who needs error checks anyway?
        self.midi.RawWrite(186 if device == 0 else 189, 0, 40 if enable == True else 41)

    # def LedGetColor(self, red, green):
    #     """
    #     Returns a Dicer compatible "color code byte"
    #     NOTE: Copied from Launchpad, won't work. The Dicer actually uses:
    #     Byte: 0b[0HHHIIII]; HHH: 3 bits hue (000=red up to 111=green) and 4 bits IIII as intensity.
    #     """
    #     led = 0
    #
    #     red = min(int(red), 3)  # make int and limit to <=3
    #     red = max(red, 0)  # no negative numbers
    #
    #     green = min(int(green), 3)  # make int and limit to <=3
    #     green = max(green, 0)  # no negative numbers
    #
    #     led |= red
    #     led |= green << 4
    #
    #     return led

    def LedCtrlRaw(self, number, hue, intensity):
        """
        Controls an LED by its raw <number>; with <hue> brightness: 0..7 (red to green)
        and <intensity> 0..15
        For LED numbers, see grid description on top of class.
        """

        if number < 0 or number > 130:
            return

        # check if that is a slave device number (>100)
        if number > 100:
            number -= 100
            cmd = 157
        else:
            cmd = 154

        # determine the "page", "hot cue", "loop" or "auto loop"
        page = number // 10
        if page > 2:
            return

        # correct the "page shifted" LED number
        number = number - (page * 10)
        if number > 10:
            return

        # limit the hue range
        hue = min(int(hue), 7)  # make int and limit to <=7
        hue = max(hue, 0)  # no negative numbers

        # limit the intensity
        intensity = min(int(intensity), 15)  # make int and limit to <=15
        intensity = max(intensity, 0)  # no negative numbers

        self.midi.RawWrite(cmd + page, number + 59, (hue << 4) | intensity)

    def ModeSet(self, device, mode):
        """
        Sets the Dicer <device> (0=master, 1=slave) to one of its six modes,
        as specified by <mode>:
         0 - "cue"
         1 - "cue, shift lock"
         2 - "loop"
         3 - "loop, shift lock"
         4 - "auto loop"
         5 - "auto loop, shift lock"
         6 - "one page"
        """

        if device < 0 or device > 1:
            return

        if mode < 0 or mode > 6:
            return

        self.midi.RawWrite(186 if device == 0 else 189, 17, mode)


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


class LaunchpadLPX(LaunchpadPro):
    """
    For 3-color "X" Launchpads
    """

    #	COLORS = {'black':0, 'off':0, 'white':3, 'red':5, 'green':17 }

    def Open(self, number=0, name="AUTO"):
        """
        Opens one of the attached Launchpad MIDI devices.
        This is one of the few devices that has different names in different OSs:
        # --
        # --   Windoze
            (b'MMSystem', b'LPX MIDI', 1, 0, 0)
            (b'MMSystem', b'MIDIIN2 (LPX MIDI)', 1, 0, 0)
            (b'MMSystem', b'LPX MIDI', 0, 1, 0)
            (b'MMSystem', b'MIDIOUT2 (LPX MIDI)', 0, 1, 0)
        # --
          macOS
            (b'CoreMIDI', b'Launchpad X LPX DAW Out', 1, 0, 0)
            (b'CoreMIDI', b'Launchpad X LPX MIDI Out', 1, 0, 0)
            (b'CoreMIDI', b'Launchpad X LPX DAW In', 0, 1, 0)
            (b'CoreMIDI', b'Launchpad X LPX MIDI In', 0, 1, 0)
        # --
          Linux [tm]
            ('ALSA', 'Launchpad X MIDI 1', 0, 1, 0)
            ('ALSA', 'Launchpad X MIDI 1', 1, 0, 0)
            ('ALSA', 'Launchpad X MIDI 2', 0, 1, 0)
            ('ALSA', 'Launchpad X MIDI 2', 1, 0, 0)
        # --
        So the old strategy of simply looking for "LPX" will not work.
        Workaround: If the user doesn't request a specific name, we'll just
        search for "Launchpad X" and "LPX"...
        """

        nameList = ["Launchpad X", "LPX"]
        if name != "AUTO":
            # mhh, better not this way
            # nameList.insert( 0, name )
            nameList = [name]
        for name in nameList:
            rval = super(LaunchpadLPX, self).Open(number=number, name=name)
            if rval:
                self.LedSetMode(1)
                return rval
        return False

    def Check(self, number=0, name="AUTO"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        See notes in "Open()" above.
        """

        nameList = ["Launchpad X", "LPX"]
        if name != "AUTO":
            # mhh, better not this way
            # nameList.insert( 0, name )
            nameList = [name]
        for name in nameList:
            rval = super(LaunchpadLPX, self).Check(number=number, name=name)
            if rval:
                return rval
        return False

    # TODO: ASkr, Undocumented!
    # TODO: return value
    def LedSetLayout(self, mode):
        """
        Sets the button layout (and codes) to the set, specified by <mode>.
        Valid options:
         00 - Session, 01 - Note Mode, 04 - Custom 1, 05 - Custom 2, 06 - Custom 3
         07 - Custom 4, 0D - DAW Faders (available if Session enabled), 7F - Programmer
        """
        ValidModes = [0x00, 0x01, 0x04, 0x05, 0x06, 0x07, 0x0d, 0x7F]
        if mode not in ValidModes:
            return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 12, 0, mode])
        time.wait(10)

    def LedSetMode(self, mode):
        """
        Selects the LPX's mode.
        <mode> -> 0 -> "Ableton Live mode"
                  1 -> "Programmer mode"	(what we need)
        """

        if mode < 0 or mode > 1:
            return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 12, 14, mode])
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
        If <blue> is omitted, this methos runs in "Classic" compatibility mode and the
        intensities, which were within 0..3 in that mode, are multiplied by 21 (0..63)
        to emulate the old brightness feeling :)
        Notice that each message requires 10 bytes to be sent. For a faster, but
        unfortunately "not-RGB" method, see "LedCtrlRawByCode()"
        LPX color data extended to 7-bit but for compatibility we still using 6-bit values
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

        self.midi.RawWriteSysEx([0, 32, 41, 2, 12, 3, 3, number, red, green, blue])

    def LedCtrlPulseByCode(self, number, colorcode=None):
        """
        Same as LedCtrlRawByCode, but with a pulsing LED.
        Pulsing can be stoppped by another Note-On/Off or SysEx message.
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
        # TODO: redundant (but needs fix for Py2 embedded anyway)
        self.midi.CloseInput()
        self.midi.CloseOutput()

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
        Unlike the Launchpad Pro, the X does indeed return the button number AND the
        pressure value. To provide visibility whether or not a button was pressed or is
        hold, a value of 255 is added to the button number.
        [ <button> + 255, <value> ].
        In contrast to the Pro, which only has one pressure value for all, the X does
        this per button. Nice.
        """

        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            # Copied over from the Pro's method.
            # Try to avoid getting flooded with pressure events
            if returnPressure == False:
                while a[0][0][0] == 160:
                    a = self.midi.ReadRaw()
                    if a == []:
                        return []

            if a[0][0][0] == 144 or a[0][0][0] == 176:
                return [a[0][0][1], a[0][0][2]]
            else:
                if returnPressure:
                    if a[0][0][0] == 160:
                        # the X returns button number AND pressure value
                        # adding 255 to make it possible to distinguish "pressed" from "pressure"
                        return [255 + a[0][0][1], a[0][0][2]]
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

            # 8/2020: Copied from the Pro.
            # 9/2020: now also _with_ pressure :)
            if returnPressure == False:
                while a[0][0][0] == 160:
                    a = self.midi.ReadRaw()
                    if a == []:
                        return []

            if a[0][0][0] == 144 or a[0][0][0] == 176 or a[0][0][0] == 160:

                if mode.lower() != "pro":
                    x = (a[0][0][1] - 1) % 10
                else:
                    x = a[0][0][1] % 10
                y = (99 - a[0][0][1]) // 10

                # now with pressure events (9/2020)
                if a[0][0][0] == 160 and returnPressure == True:
                    return [x + 255, y + 255, a[0][0][2]]
                else:
                    return [x, y, a[0][0][2]]
            else:
                return []
        else:
            return []


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


########################################################################################
### CLASS MidiFighter3D
###
###
########################################################################################
class MidiFighter3D(MidiFighter64):
    """
    For Midi Fighter 3D Gedöns

    LED AND BUTTON NUMBERS IN RAW MODE

      Button codes depend on the selected bank,
      the bottom row with the small buttons.

            +---+---+---+---+              +---+---+---+---+
            | 39|   |   | 36|              | 55|   |   | 52|
      +---+ +---+---+---+---+ +---+  +---+ +---+---+---+---+ +---+
      |   | | 43|   |   | 40| |   |  |   | | 59|   |   | 56| |   |
      |   | +---+---+---+---+ |   |  |   | +---+---+---+---+ |   |
      |   | | 47|   |   | 44| |   |  |   | | 63|   |   | 60| |   |
      +---+ +---+---+---+---+ +---+  +---+ +---+---+---+---+ +---+
            | 51|   |   | 48|              | 67|   |   | 64|
            +---+---+---+---+              +---+---+---+---+
            +---+---+---+---+              +---+---+---+---+
            |   |   |   |###|              |   |   |###|   |
            +---+---+---+---+              +---+---+---+---+

            +---+---+---+---+              +---+---+---+---+
            | 71|   |   | 68|              | 87|   |   | 84|
      +---+ +---+---+---+---+ +---+  +---+ +---+---+---+---+ +---+
      |   | | 75|   |   | 72| |   |  |   | | 91|   |   | 88| |   |
      |   | +---+---+---+---+ |   |  |   | +---+---+---+---+ |   |
      |   | | 79|   |   | 76| |   |  |   | | 95|   |   | 92| |   |
      +---+ +---+---+---+---+ +---+  +---+ +---+---+---+---+ +---+
            | 83|   |   | 80|              | 99|   |   | 96|
            +---+---+---+---+              +---+---+---+---+
            +---+---+---+---+              +---+---+---+---+
            |   |###|   |   |              |###|   |   |   |
            +---+---+---+---+              +---+---+---+---+


    LED AND BUTTON NUMBERS IN XY MODE (X/Y)

                 0   1   2   3
               +---+---+---+---+
      0        |   |1/0|   |   |
         +---+ +---+---+---+---+ +---+
      1  |   | |   |   |   |   | |   |
         |   | +---+---+---+---+ |   |
      2  |   | |   |   |   |3/2 | |   |
         +---+ +---+---+---+---+ +---+
      3        |0/3|   |   |   |
               +---+---+---+---+
               +---+---+---+---+
               |   |   |   |   |
               +---+---+---+---+
    """

    def Open(self, number=0, name="Fighter 3D"):
        """
        Opens one of the attached Launchpad MIDI devices.
        Uses search string "Fighter 3D", by default.
        """

        return super(MidiFighter3D, self).Open(number=number, name=name)

    def Check(self, number=0, name="Fighter 3D"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "Fighter 3D", by default.
        """

        return super(MidiFighter3D, self).Check(number=number, name=name)

    def ButtonStateRaw(self):
        """
        Returns the raw value of the last button change (pressed/unpressed) as a list
        [ <button>, <velocity> ], in which <button> is the raw number of the button and
        <velocity> the button state.
          >0 = button pressed; 0 = button released
        """

        if self.midi.ReadCheck():
            a = self.midi.ReadRaw()

            #    [[[ <NoteOn/Off>, <button>, 127, 0], 47610]]
            #
            #    146/147 -> NoteOn
            #    130/131 -> NoteOff
            #    127     -> fixed velocity (as set by the Midi Fighter utility )
            #
            #    Top arcade buttons on channel 3    -> 146 ON, 130 OFF
            #    Side and bank buttons on channel 4 -> 147 ON, 131 OFF

            if a[0][0][0] == 146 or a[0][0][0] == 147:
                return [a[0][0][1], a[0][0][2]]
            else:
                if a[0][0][0] == 130 or a[0][0][0] == 131:
                    return [a[0][0][1], 0]
                else:
                    return []
        else:
            return []

    def LedCtrlXY(self, x, y, color, mode=None):
        """
        Controls a grid LED by its <x>/<y> coordinates and a <color>.
         <x>/<y>  0..3
         <color>  0..127 from color table
        """

        if x < 0 or x > 3:
            return
        if y < 0 or y > 3:
            return
        if color < 0 or color > 127:
            return

        number = 39 - x  # 36 - 4 + x
        number += 4 * y

        self.midi.RawWrite(146, number, color)
        # set the mode if required; faster than calling LedCtrlRawMode()
        if mode is not None and mode > 17 and mode < 54:
            self.midi.RawWrite(147, number - 3 * 12, mode)


class LaunchpadProMk3(LaunchpadPro):
    """
    For 3-color Pro Mk3 Launchpads

    LED AND BUTTON NUMBERS IN RAW MODE

    +---+  +---+---+---+---+---+---+---+---+  +---+
    | 90|  | 91|   |   |   |   |   |   | 98|  | 99|
    +---+  +---+---+---+---+---+---+---+---+  +---+

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
           |101|102|   |   |   |   |   |108|
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
           |/10|   |   |   |   |   |   |   |        10
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
           |   |2/9|   |   |   |   |   |8/9|         9
           +---+---+---+---+---+---+---+---+
           |   |   |   |   |   |   |   |/10|        10
           +---+---+---+---+---+---+---+---+
    """

    def Open(self, number=0, name="ProMk3"):
        """
        Opens one of the attached Launchpad MIDI devices.
        Uses search string "ProMK3", by default.
        """

        retval = super(LaunchpadProMk3, self).Open(number=number, name=name)
        if retval:
            # enable Programmer's mode
            self.LedSetMode(1)

        return retval

    def Check(self, number=0, name="ProMk3"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "ProMk3", by default.
        """

        return super(LaunchpadProMk3, self).Check(number=number, name=name)

    def LedSetMode(self, mode):
        """
        Selects the ProMk3's mode.
        <mode> -> 0 -> "Ableton Live mode"
                  1 -> "Programmer mode"	(what we need)
        """

        if mode < 0 or mode > 1:
            return

        self.midi.RawWriteSysEx([0, 32, 41, 2, 14, 14, mode])
        time.wait(100)

    def LedCtrlRaw(self, number, red, green, blue=None):
        """
        Controls a grid LED by its position <number> and a color, specified by
        <red>, <green> and <blue> intensities, with can each be an integer between 0..63.
        If <blue> is omitted, this methos runs in "Classic" compatibility mode and the
        intensities, which were within 0..3 in that mode, are multiplied by 21 (0..63)
        to emulate the old brightness feeling :)
        Notice that each message requires 10 bytes to be sent. For a faster, but
        unfortunately "not-RGB" method, see "LedCtrlRawByCode()"
        ProMk3 color data extended to 7-bit but for compatibility we still using 6-bit values
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

        self.midi.RawWriteSysEx([0, 32, 41, 2, 14, 3, 3, number, red, green, blue])

    def LedCtrlPulseByCode(self, number, colorcode=None):
        """
        Same as LedCtrlRawByCode, but with a pulsing LED.
        Pulsing can be stoppped by another Note-On/Off or SysEx message.
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
                # TODO
                self.midi.RawWrite(144, (x + 1) + ((y + 1) * 10), colorcode)

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

            # 8/2020: Try to mitigate too many pressure events that a bit (yep, seems to work fine!)
            # 9/2020: XY now also with pressure event functionality
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
                if a[0][0][1] > 99:
                    y = 9
                elif a[0][0][1] < 10:
                    y = 10
                else:
                    y = (99 - a[0][0][1]) // 10

                return [x, y, a[0][0][2]]
            else:
                # TOCHK: this should be safe without checking "returnPressure"
                if a[0][0][0] == 208:
                    return [255, 255, a[0][0][1]]
                else:
                    return []
        else:
            return []

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

        # re-enter Live mode
        if self.midi.devIn is not None and self.midi.devOut is not None:
            self.LedSetMode(0)
    # TODO: redundant (but needs fix for Py2 embedded anyway)
    # self.midi.CloseInput()
    # self.midi.CloseOutput()
