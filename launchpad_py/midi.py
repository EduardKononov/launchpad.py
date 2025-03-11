import sys
import array

from pygame import midi


class Midi:
    """
    Midi singleton wrapper
    """

    # instance created
    instanceMidi = None

    def __init__(self):
        """
        Allow only one instance to be created
        """

        if Midi.instanceMidi is None:
            try:
                Midi.instanceMidi = Midi.__Midi()
            except:
                # TODO: maybe sth like sys.exit()?
                print("unable to initialize MIDI")
                Midi.instanceMidi = None

        self.devIn = None
        self.devOut = None

    def __getattr__(self, name):
        """
        Pass all unknown method calls to the inner Midi class __Midi()
        """
        return getattr(self.instanceMidi, name)

    def OpenOutput(self, midi_id):
        if self.devOut is None:
            try:
                # PyGame's default size of the buffer is 4096.
                # Removed code to tune that...
                self.devOut = midi.Output(midi_id, 0)
            except:
                self.devOut = None
                return False
        return True

    def CloseOutput(self):
        if self.devOut is not None:
            # self.devOut.close()
            del self.devOut
            self.devOut = None

    def OpenInput(self, midi_id, bufferSize=None):
        if self.devIn is None:
            try:
                # PyGame's default size of the buffer is 4096.
                if bufferSize is None:
                    self.devIn = midi.Input(midi_id)
                else:
                    # for experiments...
                    self.devIn = midi.Input(midi_id, bufferSize)
            except:
                self.devIn = None
                return False
        return True

    def CloseInput(self):
        if self.devIn is not None:
            # self.devIn.close()
            del self.devIn
            self.devIn = None

    def ReadCheck(self):
        return self.devIn.poll()

    def ReadRaw(self):
        return self.devIn.read(1)

    def RawWrite(self, stat, dat1, dat2):
        """
        sends a single, short message
        """
        self.devOut.write_short(stat, dat1, dat2)

    def RawWriteMulti(self, lstMessages):
        """
        Sends a list of messages. If timestamp is 0, it is ignored.
        Amount of <dat> bytes is arbitrary.
        [ [ [stat, <dat1>, <dat2>, <dat3>], timestamp ],  [...], ... ]
        <datN> fields are optional
        """
        self.devOut.write(lstMessages)

    # -------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------
    def RawWriteSysEx(self, lstMessage, timeStamp=0):
        """
        Sends a single system-exclusive message, given by list <lstMessage>
        The start (0xF0) and end bytes (0xF7) are added automatically.
        [ <dat1>, <dat2>, ..., <datN> ]
        Timestamp is not supported and will be sent as '0' (for now)
        """

        # There's a bug in PyGame's (Python 3) list-type message handling, so as a workaround,
        # we'll use the string-type message instead...
        # self.devOut.write_sys_ex( timeStamp, [0xf0] + lstMessage + [0xf7] ) # old Python 2

        # array.tostring() deprecated in 3.9; quickfix ahead
        try:
            self.devOut.write_sys_ex(timeStamp, array.array('B', [0xf0] + lstMessage + [0xf7]).tostring())
        except:
            self.devOut.write_sys_ex(timeStamp, array.array('B', [0xf0] + lstMessage + [0xf7]).tobytes())

    class __Midi:
        """
        The rest of the Midi class, non Midi-device specific.
        """

        def __init__(self):
            # exception handling moved up to Midi()
            midi.init()
            # but I can't remember why I put this one in here...
            midi.get_count()

        def __del__(self):
            """
            This will never be executed, because no one knows, how many Launchpad instances
            exist(ed) until we start to count them...
            """
            # midi.quit()
            pass

        def SearchDevices(self, name, output=True, input=True, quiet=True):
            """
            Returns a list of devices that matches the string 'name' and has in- or outputs.
            """

            ret = []

            for i in range(midi.get_count()):
                md = midi.get_device_info(i)
                if name.lower() in str(md[1].lower()):
                    if not quiet:
                        print('%2d' % (i), md)
                        sys.stdout.flush()
                    if output == True and md[3] > 0:
                        ret.append(i)
                    if input == True and md[2] > 0:
                        ret.append(i)

            return ret

        def SearchDevice(self, name, output=True, input=True, number=0):
            """
            Returns the first device that matches the string 'name'.
            NEW2015/02: added number argument to pick from several devices (if available)
            """
            ret = self.SearchDevices(name, output, input)

            if number < 0 or number >= len(ret):
                return None

            return ret[number]

        def GetTime(self):
            """
            Return MIDI time
            """
            return midi.time()
