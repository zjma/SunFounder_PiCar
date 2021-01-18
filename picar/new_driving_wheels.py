import RPi.GPIO as GPIO
from .SunFounder_PCA9685 import PCA9685

_pinOfWheel = {
	'L': 27,
	'R': 17,
}

_pwmChannelOfWheel = {
	'L': 4,
	'R': 5,
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(_pinOfWheel['L'], GPIO.OUT)
GPIO.setup(_pinOfWheel['R'], GPIO.OUT)
_pwm = PCA9685.PWM(bus_number=1)

def setWheelSpeed(wheel, speed):
	assert type(speed)==int
	assert speed<=100
	assert speed>=-100
	assert wheel in ('L','R')
	GPIO.output(_pinOfWheel[wheel], speed>=0)
	_pwm.write(_pwmChannelOfWheel[wheel], 0, int(4095*abs(speed)/100))

def setSpeed(leftSpeed, rightSpeed):
	'''Set the speed (relative to top speed, -100 to 100) for both wheel.'''
	setWheelSpeed('L', leftSpeed)
	setWheelSpeed('R', rightSpeed)

#Init
setSpeed(0,0)
