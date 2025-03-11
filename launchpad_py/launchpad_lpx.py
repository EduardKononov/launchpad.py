from pygame import time

from launchpad_py import LaunchpadPro

__all__ = ['LaunchpadLPX']


class LaunchpadLPX(LaunchpadPro):
    """
    For 3-color "X" Launchpads
    """

    #	COLORS = {'black':0, 'off':0, 'white':3, 'red':5, 'green':17 }

    def Open(self, number=0, name="AUTO"):
        """
        Opens one of the attached Launchpad MIDI devices.
        This is one of the few devices that has different names in different OSs:

         Windows
            (b'MMSystem', b'LPX MIDI', 1, 0, 0)
            (b'MMSystem', b'MIDIIN2 (LPX MIDI)', 1, 0, 0)
            (b'MMSystem', b'LPX MIDI', 0, 1, 0)
            (b'MMSystem', b'MIDIOUT2 (LPX MIDI)', 0, 1, 0)

          macOS
            (b'CoreMIDI', b'Launchpad X LPX DAW Out', 1, 0, 0)
            (b'CoreMIDI', b'Launchpad X LPX MIDI Out', 1, 0, 0)
            (b'CoreMIDI', b'Launchpad X LPX DAW In', 0, 1, 0)
            (b'CoreMIDI', b'Launchpad X LPX MIDI In', 0, 1, 0)

          Linux [tm]
            ('ALSA', 'Launchpad X MIDI 1', 0, 1, 0)
            ('ALSA', 'Launchpad X MIDI 1', 1, 0, 0)
            ('ALSA', 'Launchpad X MIDI 2', 0, 1, 0)
            ('ALSA', 'Launchpad X MIDI 2', 1, 0, 0)

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
