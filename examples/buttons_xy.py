#!/usr/bin/env python
#
# Quick button test.
# Works with these Launchpads: Mk1, Mk2, Mini Mk3, S/Mini, Pro, Pro Mk3
# And these:                   Midi Figther 64
# 
#
# FMMT666(ASkr) 7/2013..8/2020
# www.askrprojects.net
#

import sys
import time

import launchpad_py.dicer
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


def main():

	mode = None

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

	elif launchpad_py.launchpad_mini_mk3.LaunchpadMiniMk3().check(1):
		lp = launchpad_py.launchpad_mini_mk3.LaunchpadMiniMk3()
		if lp.open(1):
			print("Launchpad Mini Mk3")
			mode = "MiniMk3"

	elif launchpad_py.launchpad_lpx.LaunchpadLPX().check(1):
		lp = launchpad_py.launchpad_lpx.LaunchpadLPX()
		if lp.open(1):
			print("Launchpad X")
			mode = "LPX"
			
	elif launchpad_py.launchpad_mk2.LaunchpadMk2().check(0):
		lp = launchpad_py.launchpad_mk2.LaunchpadMk2()
		if lp.open(0):
			print("Launchpad Mk2")
			mode = "Mk2"

	# elif launchpad.LaunchControlXL().Check( 0 ):
	# 	lp = launchpad.LaunchControlXL()
	# 	if lp.Open( 0 ):
	# 		print("Launch Control XL")
	# 		mode = "XL"
			
	# elif launchpad.LaunchKeyMini().Check( 0 ):
	# 	lp = launchpad.LaunchKeyMini()
	# 	if lp.Open( 0 ):
	# 		print("LaunchKey (Mini)")
	# 		mode = "LKM"

	elif launchpad_py.dicer.Dicer().check(0):
		lp = launchpad_py.dicer.Dicer()
		if lp.open(0):
			print("Dicer")
			mode = "Dcr"

	elif launchpad_py.midi_fighter64.MidiFighter64().check(0):
		lp = launchpad_py.midi_fighter64.MidiFighter64()
		if lp.open(0):
			print("Midi Fighter 64")
			mode = "F64"

	elif launchpad_py.launchpad.Launchpad().check(0):
		lp = launchpad_py.launchpad.Launchpad()
		if lp.open(0):
			print("Launchpad Mk1/S/Mini")
			mode = "Mk1"

	if mode is None:
		print("Did not find any Launchpads, meh...")
		return

	print("QUIT: Push a single button for longer than 3s and release it.")

	lastBut = (-99,-99)
	tStart = time.time()
	while True:
		if mode == 'Pro' or mode == 'ProMk3':
			buts = lp.ButtonStateXY( mode = 'pro')
		else:
			buts = lp.ButtonStateXY()

		if buts != []:
			print( buts[0], buts[1], buts[2] )

			# quit?
			if buts[2] > 0:
				lastBut = ( buts[0], buts[1] )
				tStart = time.time()
			else:
				if lastBut == ( buts[0], buts[1] ) and (time.time() - tStart) > 2:
					break


	print("bye ...")

	lp.reset() # turn all LEDs off
	lp.close() # close the Launchpad (will quit with an error due to a PyGame bug)

	
if __name__ == '__main__':
	main()

