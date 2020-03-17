# The MIT License (MIT)
#
# Copyright (c) 2016 Radomir Dopieralski, written for Adafruit Industries
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_pca9685`
====================================================

Driver for the PCA9685 PWM control IC. Its commonly used to control servos, leds and motors.

.. seealso:: The `Adafruit CircuitPython Motor library
    <https://github.com/adafruit/Adafruit_CircuitPython_Motor>`_ can be used to control the PWM
    outputs for specific uses instead of generic duty_cycle adjustments.

* Author(s): Scott Shawcroft

Implementation Notes
--------------------

**Hardware:**

* Adafruit `16-Channel 12-bit PWM/Servo Driver - I2C interface - PCA9685
  <https://www.adafruit.com/product/815>`_ (Product ID: 815)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the ESP8622 and M0-based boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PCA9685.git"

import time

from adafruit_register.i2c_struct import UnaryStruct
from adafruit_register.i2c_struct_array import StructArray
from adafruit_bus_device import i2c_device


class PWMChannel:
    """A single PCA9685 channel that matches the :py:class:`~pulseio.PWMOut` API."""

    def __init__(self, pca, index):
        self._pca = pca
        self._index = index

    @property
    def frequency(self):
        """The overall PWM frequency in Hertz (read-only).
        A PWMChannel's frequency cannot be set individually.
        All channels share a common frequency, set by PCA9685.frequency."""
        return self._pca.frequency

    @frequency.setter
    def frequency(self, _):
        raise NotImplementedError("frequency cannot be set on individual channels")

    @property
    def duty_cycle(self):
        """16 bit value that dictates how much of one cycle is high (1) versus low (0). 0xffff will
           always be high, 0 will always be low and 0x7fff will be half high and then half low."""
        pwm = self._pca.pwm_regs[self._index]
        if pwm[0] == 0x1000:
            return 0xFFFF
        return pwm[1] << 4

    @duty_cycle.setter
    def duty_cycle(self, value):
        if not 0 <= value <= 0xFFFF:
            raise ValueError("Out of range")

        if value == 0xFFFF:
            self._pca.pwm_regs[self._index] = (0x1000, 0)
        else:
            # Shift our value by four because the PCA9685 is only 12 bits but our value is 16
            value = (value + 1) >> 4
            self._pca.pwm_regs[self._index] = (0, value)


class PCAChannels:  # pylint: disable=too-few-public-methods
    """Lazily creates and caches channel objects as needed. Treat it like a sequence."""

    def __init__(self, pca):
        self._pca = pca
        self._channels = [None] * len(self)

    def __len__(self):
        return 16

    def __getitem__(self, index):
        if not self._channels[index]:
            self._channels[index] = PWMChannel(self._pca, index)
        return self._channels[index]


class PCA9685:
    """
    Initialise the PCA9685 chip at ``address`` on ``i2c_bus``.

    The internal reference clock is 25mhz but may vary slightly with environmental conditions and
    manufacturing variances. Providing a more precise ``reference_clock_speed`` can improve the
    accuracy of the frequency and duty_cycle computations. See the ``calibration.py`` example for
    how to derive this value by measuring the resulting pulse widths.

    :param ~busio.I2C i2c_bus: The I2C bus which the PCA9685 is connected to.
    :param int address: The I2C address of the PCA9685.
    :param int reference_clock_speed: The frequency of the internal reference clock in Hertz.
    """

    # Registers:
    mode1_reg = UnaryStruct(0x00, "<B")
    prescale_reg = UnaryStruct(0xFE, "<B")
    pwm_regs = StructArray(0x06, "<HH", 16)

    def __init__(self, i2c_bus, *, address=0x40, reference_clock_speed=25000000):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        self.channels = PCAChannels(self)
        """Sequence of 16 `PWMChannel` objects. One for each channel."""
        self.reference_clock_speed = reference_clock_speed
        """The reference clock speed in Hz."""
        self.reset()

    def reset(self):
        """Reset the chip."""
        self.mode1_reg = 0x00  # Mode1

    @property
    def frequency(self):
        """The overall PWM frequency in Hertz."""
        return self.reference_clock_speed / 4096 / self.prescale_reg

    @frequency.setter
    def frequency(self, freq):
        prescale = int(self.reference_clock_speed / 4096.0 / freq + 0.5)
        if prescale < 3:
            raise ValueError("PCA9685 cannot output at the given frequency")
        old_mode = self.mode1_reg  # Mode 1
        self.mode1_reg = (old_mode & 0x7F) | 0x10  # Mode 1, sleep
        self.prescale_reg = prescale  # Prescale
        self.mode1_reg = old_mode  # Mode 1
        time.sleep(0.005)
        self.mode1_reg = old_mode | 0xA1  # Mode 1, autoincrement on

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.deinit()

    def deinit(self):
        """Stop using the pca9685."""
        self.reset()
