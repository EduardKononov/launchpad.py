#!/usr/bin/env python
#
# Resets the Pro Mk3 (into Live mode)
# 
#
# FMMT666(ASkr) 7/2013..8/2020
# www.askrprojects.net
#

import sys

import launchpad_py.launchpad_pro_mk3

try:
	import launchpad_py as launchpad
except ImportError:
	try:
		import launchpad
	except ImportError:
		sys.exit("error loading launchpad_to_refactor.py")


def main():

	if launchpad_py.launchpad_pro_mk3.LaunchpadProMk3().check(0):
		lp = launchpad_py.launchpad_pro_mk3.LaunchpadProMk3()
		if lp.open(0):
			print("Launchpad Pro Mk3 found")
			lp.close()
	else:
		print("Meh, did not find a Launchpad Pro Mk3")


	
if __name__ == '__main__':
	main()

