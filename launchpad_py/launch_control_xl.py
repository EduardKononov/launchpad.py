from launchpad_py.launchpad_base import LaunchpadBase

__all__ = ['LaunchControlXL']


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
        Opens one of the attached Control XL MIDI devices.
        Uses search string "Control XL", by default.
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
        elif x == 8:
            # device, mute, solo, record
            if y > 2:
                index = 37 + y
            # up
            elif y == 1:
                index = 44
            # left
            elif y == 2:
                index = 46
            else:
                return
        elif x == 9:
            # device, mute, solo, record
            if y > 2:
                index = 37 + y
            # down
            elif y == 1:
                index = 45
            # right
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

            # pressed
            if a[0][0][0] == 144:
                return [a[0][0][1], True, 127]
            # released
            elif a[0][0][0] == 128:
                return [a[0][0][1], False, 0]
            # potentiometers and the four cursor buttons
            elif a[0][0][0] == 176:
                # cursor buttons
                if a[0][0][1] >= 104 and a[0][0][1] <= 107:
                    if a[0][0][2] > 0:
                        return [a[0][0][1], True, a[0][0][2]]
                    else:
                        return [a[0][0][1], False, 0]
                # potentiometers
                else:
                    return [a[0][0][1], a[0][0][2], 0]
            else:
                return []
        else:
            return []
