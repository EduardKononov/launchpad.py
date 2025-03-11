from launchpad_py.launchpad_base import LaunchpadBase

__all__ = ['Dicer']


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
