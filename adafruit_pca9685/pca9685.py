import ustruct
import time

from adafruit_register import i2c_struct
from adafruit_bus_device import i2c_device


class PCA9685:
    # Registers:
    mode1_reg = i2c_struct.UnaryStruct(0x00, '<B')
    prescale_reg = i2c_struct.UnaryStruct(0xFE, '<B')
    pwm_regs = (i2c_struct.Struct(0x06, '<HH'), # PWM 0
                i2c_struct.Struct(0x0A, '<HH'), # PWM 1
                i2c_struct.Struct(0x0E, '<HH'), # PWM 2
                i2c_struct.Struct(0x12, '<HH'), # PWM 3
                i2c_struct.Struct(0x16, '<HH'), # PWM 4
                i2c_struct.Struct(0x1A, '<HH'), # PWM 5
                i2c_struct.Struct(0x1E, '<HH'), # PWM 6
                i2c_struct.Struct(0x22, '<HH'), # PWM 7
                i2c_struct.Struct(0x26, '<HH'), # PWM 8
                i2c_struct.Struct(0x2A, '<HH'), # PWM 9
                i2c_struct.Struct(0x2E, '<HH'), # PWM 10
                i2c_struct.Struct(0x32, '<HH'), # PWM 11
                i2c_struct.Struct(0x36, '<HH'), # PWM 12
                i2c_struct.Struct(0x3A, '<HH'), # PWM 13
                i2c_struct.Struct(0x3E, '<HH'), # PWM 14
                i2c_struct.Struct(0x42, '<HH')) # PWM 15

    def __init__(self, i2c, address=0x40):
        self.i2c_device = i2c_device.I2CDevice(i2c, address)
        self.reset()

    def reset(self):
        self.mode1_reg = 0x00 # Mode1

    def freq(self, freq=None):
        if freq is None:
            return int(25000000.0 / 4096 / (self.prescale_reg - 0.5))
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self.mode1_reg # Mode 1
        self.mode1_reg = (old_mode & 0x7F) | 0x10 # Mode 1, sleep
        self.prescale_reg = prescale # Prescale
        self.mode1_reg = old_mode # Mode 1
        time.sleep(0.005)
        self.mode1_reg = old_mode | 0xa1 # Mode 1, autoincrement on

    def pwm(self, index, on=None, off=None):
        if on is None or off is None:
            return self.pwm_regs[index].__get__(self)
        self.pwm_regs[index].__set__(self, (on, off))

    def duty(self, index, value=None, invert=False):
        if value is None:
            pwm = self.pwm(index)
            if pwm == (0, 4096):
                value = 0
            elif pwm == (4096, 0):
                value = 4095
            value = pwm[1]
            if invert:
                value = 4095 - value
            return value
        if not 0 <= value <= 4095:
            raise ValueError("Out of range")
        if invert:
            value = 4095 - value
        if value == 0:
            self.pwm(index, 0, 4096)
        elif value == 4095:
            self.pwm(index, 4096, 0)
        else:
            self.pwm(index, 0, value)
