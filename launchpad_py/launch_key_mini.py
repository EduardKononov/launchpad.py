from launchpad_py.launchpad_base import LaunchpadBase

__all__ = ['LaunchKeyMini']


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

    def open(self, number=0, name="LaunchKey"):
        """
        Opens one of the attached LaunchKey devices.
        Uses search string "LaunchKey", by default.
        """
        retval = super(LaunchKeyMini, self).open(number=number, name=name)
        return retval

    def check(self, number=0, name="LaunchKey"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "LaunchKey", by default.
        """
        return super(LaunchKeyMini, self).check(number=number, name=name)

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
        return self.flush_buttons()

    def InputChanged(self):
        """
        Returns True if an event occured.
        """
        return self.midi.ReadCheck()
