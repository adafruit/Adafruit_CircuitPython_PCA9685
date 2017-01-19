Motor Driver
************

.. module:: motor

.. class:: DCMotors(i2c, address=0x40, freq=1600)

    Control the motor driver.

    The `freq` argument allows setting PWM frequency. Most motors should be
    fine with the default.

    .. method:: speed(index, [value])

        Set or get the motor's speed.

        Negative values make the motor spin backwards. Zero releases the motor.

    .. method:: brake(index)

        Brake the motor.
