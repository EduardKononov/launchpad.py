from launchpad_py import LaunchControlXL

__all__ = ['LaunchControl']


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
