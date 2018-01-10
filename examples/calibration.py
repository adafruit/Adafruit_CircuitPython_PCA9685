# This advanced example can be used to compute a more precise reference_clock_speed. Use an
# oscilloscope or logic analyzer to measure the signal frequency and type the results into the
# prompts. At the end it'll give you a more precise value around 25 mhz for your reference clock
# speed.

import time

from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 100hz.
pca.frequency = 100

input("Press enter when ready to measure default frequency.")

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
print("Running with default calibration")
pca.channels[0].duty_cycle = 0x7fff
time.sleep(1)
pca.channels[0].duty_cycle = 0

measured_frequency = float(input("Frequency measured: "))
print()

pca.reference_clock_speed = pca.reference_clock_speed * (measured_frequency / pca.frequency)
# Set frequency again so we can get closer. Reading it back will produce the real value.
pca.frequency = 100

input("Press enter when ready to measure coarse calibration frequency.")
pca.channels[0].duty_cycle = 0x7fff
time.sleep(1)
pca.channels[0].duty_cycle = 0
measured_after_calibration = float(input("Frequency measured: "))
print()

reference_clock_speed = measured_after_calibration * 4096 * pca.prescale_reg

print("Real reference clock speed: {0:.0f}".format(reference_clock_speed))
