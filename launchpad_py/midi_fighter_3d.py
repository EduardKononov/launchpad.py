from launchpad_py import MidiFighter64

__all__ = ['MidiFighter3D']


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

    def open(self, number=0, name="Fighter 3D"):
        """
        Opens one of the attached Launchpad MIDI devices.
        Uses search string "Fighter 3D", by default.
        """

        return super(MidiFighter3D, self).open(number=number, name=name)

    def check(self, number=0, name="Fighter 3D"):
        """
        Checks if a device exists, but does not open it.
        Does not check whether a device is in use or other, strange things...
        Uses search string "Fighter 3D", by default.
        """

        return super(MidiFighter3D, self).check(number=number, name=name)

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
