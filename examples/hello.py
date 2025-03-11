#!/usr/bin/env python
#
# Quick usage of "launchpad_to_refactor.py", LEDs and buttons.
# Works with all Launchpads: Mk1, Mk2, Mini Mk3, S/Mini, Pro, Pro Mk3, XL and LaunchKey
# And these: Midifighter 64
# 
#
# FMMT666(ASkr) 7/2013..8/2020
# www.askrprojects.net
#

import sys

import launchpad_py.dicer
import launchpad_py.launch_control_xl
import launchpad_py.launch_key_mini
import launchpad_py.launchpad
import launchpad_py.launchpad_lpx
import launchpad_py.launchpad_mini_mk3
import launchpad_py.launchpad_mk2
import launchpad_py.launchpad_pro
import launchpad_py.launchpad_pro_mk3
import launchpad_py.midi_fighter64

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("error loading launchpad_to_refactor.py")

import random
from pygame import time


def main():

	mode = None

	# create an instance for the Pro
	if launchpad_py.launchpad_pro.LaunchpadPro().check(0):
		lp = launchpad_py.launchpad_pro.LaunchpadPro()
		if lp.open(0):
			print("Launchpad Pro")
			mode = "Pro"

	elif launchpad_py.launchpad_pro_mk3.LaunchpadProMk3().check(0):
		lp = launchpad_py.launchpad_pro_mk3.LaunchpadProMk3()
		if lp.open(0):
			print("Launchpad Pro Mk3")
			mode = "ProMk3"

	# experimental MK3 implementation
	# The MK3 has two MIDI instances per device; we need the 2nd one.
	# If you have two MK3s attached, its "1" for the first and "3" for the 2nd device
	elif launchpad_py.launchpad_mini_mk3.LaunchpadMiniMk3().check(1):
		lp = launchpad_py.launchpad_mini_mk3.LaunchpadMiniMk3()
		if lp.open(1, "minimk3"):
			print("Launchpad Mini Mk3")
			mode = "Pro"

	# experimental LPX implementation
	# Like the Mk3, the LPX also has two MIDI instances per device; we need the 2nd one.
	# If you have two LPXs attached, its "1" for the first and "3" for the 2nd device
	elif launchpad_py.launchpad_lpx.LaunchpadLPX().check(1):
		lp = launchpad_py.launchpad_lpx.LaunchpadLPX()
		if lp.open(1, "lpx"):
			print("Launchpad X")
			mode = "Pro"
			
	elif launchpad_py.launchpad_mk2.LaunchpadMk2().check(0):
		lp = launchpad_py.launchpad_mk2.LaunchpadMk2()
		if lp.open(0, "mk2"):
			print("Launchpad Mk2")
			mode = "Mk2"

	elif launchpad_py.launch_control_xl.LaunchControlXL().check(0):
		lp = launchpad_py.launch_control_xl.LaunchControlXL()
		if lp.open(0, "control xl"):
			print("Launch Control XL")
			mode = "XL"
			
	elif launchpad_py.launch_key_mini.LaunchKeyMini().check(0):
		lp = launchpad_py.launch_key_mini.LaunchKeyMini()
		if lp.open(0, "launchkey"):
			print("LaunchKey (Mini)")
			mode = "LKM"

	elif launchpad_py.dicer.Dicer().check(0):
		lp = launchpad_py.dicer.Dicer()
		if lp.open(0, "dicer"):
			print("Dicer")
			mode = "Dcr"

	elif launchpad_py.midi_fighter64.MidiFighter64().check(0):
		lp = launchpad_py.midi_fighter64.MidiFighter64()
		if lp.open(0):
			print("Midi Fighter 64")
			mode = "MF64"

	else:
		lp = launchpad_py.launchpad.Launchpad()
		if lp.open():
			print("Launchpad Mk1/S/Mini")
			mode = "Mk1"

	if mode is None:
		print("Did not find any Launchpads, meh...")
		return


	# scroll a string from right to left
	if mode == "Mk1":
		lp.LedCtrlString( "HENLO!", 0, 3, -1 )
	# the MF64's methods are not compatible with the Launchpad ones
	elif mode == "MF64":
		lp.LedCtrlString( "HENLO!", 5, 0, -1, waitms = 50 )
	# for all others except the XL and the LaunchKey
	elif mode != "XL" and mode != "LKM" and mode != "Dcr":
		lp.LedCtrlString( "HENLO!", 0, 63, 0, -1, waitms = 50 )


	# random output
	if mode == "LKM":
		print("The LaunchKey(Mini) does not (yet) support LED activation, but you")
		print("can push some buttons or rotate some knobes now...")
		print("Auto exit if first number reaches 0")
	else:
		print("---\nRandom madness. Create some events. Stops after reaching 0 (first number)")
		print("Notice that sometimes, old Mk1 units don't recognize any button")
		print("events before you press one of the (top) automap buttons")
		print("(or power-cycle the unit...).")

	# Clear the buffer because the Launchpad remembers everything :-)
	lp.flush_buttons()

	# Lightshow
	if mode == "XL" or mode == "LKM":
		butHit = 100
	elif mode == "Dcr":
		butHit = 30
	else:
		butHit = 10
		
	while 1:
		if mode == "Mk1" or mode == "XL":
			lp.LedCtrlRaw( random.randint(0,127), random.randint(0,3), random.randint(0,3) )
		elif mode == "Dcr":
			lp.LedCtrlRaw( random.randint(0,130), random.randint(0,7), random.randint(0,15) )
		elif mode == "MF64":
			lp.LedCtrlRaw( random.randint(36,99), random.randint(0,127) )
		elif mode != "LKM":
			lp.LedCtrlRaw( random.randint(0,127), random.randint(0,63), random.randint(0,63), random.randint(0,63) )
		
		time.wait( 5 )
		
		if mode == "XL" or mode == "LKM":
			but = lp.InputStateRaw()
		else:
			but = lp.ButtonStateRaw()

		if but != []:
			butHit -= 1
			if butHit < 1:
				break
			print( butHit, " event: ", but )

	# now quit...
	print("Quitting might raise a 'Bad Pointer' error (~almost~ nothing to worry about...:).\n\n")

	lp.reset() # turn all LEDs off
	lp.close() # close the Launchpad (will quit with an error due to a PyGame bug)

	
if __name__ == '__main__':
	main()

