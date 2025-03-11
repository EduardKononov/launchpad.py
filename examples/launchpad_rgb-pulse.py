#!/usr/bin/python
#
# Stupid flashing/pulsing demo.
# Works with Mk2, Mini Mk3, Pro, X
# 
#
# FMMT666(ASkr) 10/2018..8/2020
# www.askrprojects.net
#

import sys

import launchpad_py.launchpad
import launchpad_py.launchpad_lpx
import launchpad_py.launchpad_mini_mk3
import launchpad_py.launchpad_pro
import launchpad_py.launchpad_pro_mk3

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

	# create an instance
	lp = launchpad_py.launchpad.Launchpad()

	# check what we have here and override lp if necessary
	if lp.check(0, "pad pro"):
		lp = launchpad_py.launchpad_pro.LaunchpadPro()
		if lp.open(0, "pad pro"):
			print("Launchpad Pro")
			mode = "Pro"

	elif lp.check(0, "promk3"):
		lp = launchpad_py.launchpad_pro_mk3.LaunchpadProMk3()
		if lp.open(0):
			print("Launchpad Pro Mk3")
			mode = "ProMk3"
			

	elif lp.check(1, "minimk3"):
		lp = launchpad_py.launchpad_mini_mk3.LaunchpadMiniMk3()
		if lp.open(1, "minimk3"):
			print("Launchpad Mk3")
			mode = "Mk3"

	elif lp.check(1, "launchpad x") or lp.check(1, "lpx"):
		lp = launchpad_py.launchpad_lpx.LaunchpadLPX()
		if lp.open(1):
			print("Launchpad X")
			mode = "LPX"

	if mode is None:
		print("Did not find any compatible Launchpads, meh...")
		return

	# set flashing/pulsing frequency to 240bpm
	lp.led_ctrl_bpm(240)

	# stupid lightshow from here on...
	for y in range(8):
		for x in range(8):
			lp.LedCtrlXYByCode( 7-x, 8-y, 5 if y < 4 else 13)
			lp.LedCtrlXYByCode( x, y+1, 21 if y < 4 else 13)
			time.wait(50)

	time.wait(1000)

	for y in range(8):
		for x in range(8):
			lp.LedCtrlFlashXYByCode( x, y+1, 0 )

	time.wait(3000)

	for y in range(8):
		for x in range(8):
			lp.LedCtrlPulseXYByCode( x, y+1, 53 )

	time.wait(3000)

	for x in range(4):
		for y in range(8):
			lp.LedCtrlXYByCode( 7-x, 8-y, random.randint(0, 127) )
			lp.LedCtrlFlashXYByCode( 7-x, 8-y, random.randint(0, 127) )
			lp.LedCtrlXYByCode( x, y+1, random.randint(0, 127) )
			lp.LedCtrlFlashXYByCode( x, y+1, random.randint(0, 127) )
			time.wait(250)

	time.wait(3000)


	lp.reset() # turn all LEDs off
	lp.close() # close the Launchpad (will quit with an error due to a PyGame bug)

	
if __name__ == '__main__':
	main()

