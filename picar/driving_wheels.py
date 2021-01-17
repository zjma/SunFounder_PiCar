#!/usr/bin/env python
from .SunFounder_TB6612 import TB6612
from .SunFounder_PCA9685 import PCA9685
from .import filedb

class Driving_Wheels(object):
	''' Wheels control class '''
	Motor_A = 17
	Motor_B = 27

	PWM_A = 4
	PWM_B = 5

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "back_wheels.py":'

	def __init__(self, debug=False, bus_number=1, db="config"):
		''' Init the direction channel and pwm channel '''
		self.forward_A = True
		self.forward_B = True

		self.db = filedb.fileDB(db=db)

		self.forward_A = int(self.db.get('forward_A', default_value=1))
		self.forward_B = int(self.db.get('forward_B', default_value=1))

		self.left_wheel = TB6612.Motor(self.Motor_A, offset=self.forward_A)
		self.right_wheel = TB6612.Motor(self.Motor_B, offset=self.forward_B)

		self.pwm = PCA9685.PWM(bus_number=bus_number)
		def _set_a_pwm(value):
			pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
			self.pwm.write(self.PWM_A, 0, pulse_wide)

		def _set_b_pwm(value):
			pulse_wide = int(self.pwm.map(value, 0, 100, 0, 4095))
			self.pwm.write(self.PWM_B, 0, pulse_wide)

		self.left_wheel.pwm  = _set_a_pwm
		self.right_wheel.pwm = _set_b_pwm

		self.debug = debug
		self._debug_('Set left wheel to #%d, PWM channel to %d' % (self.Motor_A, self.PWM_A))
		self._debug_('Set right wheel to #%d, PWM channel to %d' % (self.Motor_B, self.PWM_B))

	def _debug_(self,message):
		if self._DEBUG:
			print(self._DEBUG_INFO,message)

	def setStatus(self, leftSpeed, rightSpeed):
		''' Set the status for both wheels.
		@param leftSpeed	An integer between -100 to +100
		@param rightSpeed	An integer between -100 to +100.
		'''
		self.setWheelStatus(self.right_wheel, -leftSpeed)
		self.setWheelStatus(self.left_wheel, -rightSpeed)

	def setWheelStatus(self, wheel, targetSpeed):
		targetSpeed = int(targetSpeed)
		targetSpeed = max(min(targetSpeed, 100), -100)
		wheel.speed = abs(targetSpeed)
		if targetSpeed > 0:
			wheel.forward()
		elif targetSpeed < 0:
			wheel.backward()
		else:
			wheel.stop()

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
			self.left_wheel.debug = True
			self.right_wheel.debug = True
			self.pwm.debug = True
		else:
			print(self._DEBUG_INFO, "Set debug off")
			self.left_wheel.debug = False
			self.right_wheel.debug = False
			self.pwm.debug = False

	def ready(self):
		''' Get the back wheels to the ready position. (stop) '''
		self._debug_('Turn to "Ready" position')
		self.left_wheel.offset = self.forward_A
		self.right_wheel.offset = self.forward_B
		self.setStatus(0,0)

	def calibration(self):
		''' Get the front wheels to the calibration position. '''
		self._debug_('Turn to "Calibration" position')
		self.speed = 50
		self.forward()
		self.cali_forward_A = self.forward_A
		self.cali_forward_B = self.forward_B

	def cali_left(self):
		''' Reverse the left wheels forward direction in calibration '''
		self.cali_forward_A = (1 + self.cali_forward_A) & 1
		self.left_wheel.offset = self.cali_forward_A
		self.forward()

	def cali_right(self):
		''' Reverse the right wheels forward direction in calibration '''
		self.cali_forward_B = (1 + self.cali_forward_B) & 1
		self.right_wheel.offset = self.cali_forward_B
		self.forward()

	def cali_ok(self):
		''' Save the calibration value '''
		self.forward_A = self.cali_forward_A
		self.forward_B = self.cali_forward_B
		self.db.set('forward_A', self.forward_A)
		self.db.set('forward_B', self.forward_B)
		self.setStatus(0,0)
