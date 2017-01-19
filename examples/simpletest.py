from board import *
# Use this import for ESP8266 and other boards with software I2C interfaces:
import bitbangio as io
# Or use this import for SAMD21 and boards with a native hardware I2C interace:
#import nativeio as io


from adafruit_pca9685 import pca9685


i2c = io.I2C(SCL, SDA)

pca = pca9685.PCA9685(i2c)
