#!/usr/bin/env python
'''
**********************************************************************
* Filename    : back_wheels.py
* Description : A module to control the back wheels of RPi Car
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
*               Cavon    2016-11-04    fix for submodules
**********************************************************************
'''

from .SunFounder_TB6612 import TB6612
from .SunFounder_PCA9685 import PCA9685

class LeftWheel(object):
	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "LeftWheel":'

	def __init__(self, debug=False, bus_number=1, db="config"):
		''' Init the direction channel and pwm channel '''

		self.motor = TB6612.Motor(17, offset=False)
		self.pwm = PCA9685.PWM(bus_number=bus_number)
		def _set_a_pwm(value):
			pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
			self.pwm.write(4, 0, pulse_wide)

		self.motor.pwm  = _set_a_pwm

		self._speed = 0

		self.debug = debug

	def _debug_(self,message):
		if self._DEBUG:
			print(self._DEBUG_INFO,message)

	def forward(self):
		self.motor.forward()

	def backward(self):
		self.motor.backward()

	def stop(self):
		self.motor.stop()

	@property
	def speed(self, speed):
		return self._speed

	@speed.setter
	def speed(self, speed):
		self._speed = speed
		self.motor.speed = self._speed

	@property
	def debug(self):
		return self._DEBUG

	@debug.setter
	def debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print(self._DEBUG_INFO, "Set debug on")
			self.motor.debug = True
			self.pwm.debug = True
		else:
			print(self._DEBUG_INFO, "Set debug off")
			self.motor.debug = False
			self.pwm.debug = False

	def ready(self):
		''' Get the back wheels to the ready position. (stop) '''
		self._debug_('Turn to "Ready" position')
		self.motor.offset = self.forward_A
		self.stop()
