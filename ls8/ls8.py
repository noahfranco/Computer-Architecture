#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load()
cpu.run()

# *** Plan ***
#
# create a run funciton on the cpu.py file and make it run 
# create HLT for memory 
# Create a LDI pointer to adress memory 
# Create a PRN to print our file