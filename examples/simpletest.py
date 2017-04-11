from board import *
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import pca9685

# Create the I2C bus interface.
i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = pca9685.PCA9685(i2c)

# Set the PWM frequency to 60hz.
pca.freq = 60

# Set the PWM duty cycle for channel zero to 50% (i.e. half of
# the full 12-bit 4095 value)
pca.pwm(1, 2048)
