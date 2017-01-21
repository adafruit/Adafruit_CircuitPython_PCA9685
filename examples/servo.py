import time

from board import *
# Use this import for ESP8266 and other boards with software I2C interfaces:
import bitbangio as io
# Or use this import for SAMD21 and boards with a native hardware I2C interace:
#import nativeio as io

# Import the PCA9685 servo module.
from adafruit_pca9685 import servo


# Create the I2C bus interface.
i2c = io.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
servos = servo.Servos(i2c)

# Loop forever moving servo 0 between its extremes.
while True:
    servos.position(0, us=1000)  # 1000us period is one extreme
    time.sleep(1)
    servos.position(0, us=2000)  # 2000us period is opposite extreme
    time.sleep(1)
