Servo Driver
************

.. module:: servo

.. class:: Servos(i2c, address=0x40, freq=50, min_us=600, max_us=2400, degrees=180)

    Allows controlling up to 16 hobby servos.

    The `freq` argument sets the PWM signal frequency in Hz. Analog servos
    usually expect this to be 50, but digital servos can often handle higher
    frequencies, resulting in smoother movements.

    The `min_us` and `max_us` arguments set the range of the singnal's duty
    that the servo accepts. This is different between different servo models,
    but usually they are centerd at 1500µs.

    The `degrees` argument specifies the physical range of the servo
    corresponding to the signal's duty range specified before. It is used to
    calculate signal's duty when the angle is specified in degrees or radians.


    .. method:: position(index, [degrees|radians|us|duty])

        Get or set the servo position. The position can be specified in
        degrees (the default), radians, microseconds or directly as a number
        between 0 and 4095 signifying the duty cycle. It will be automatically
        clamped to the minimum and maximum range allowed.

        When getting the position, it will always be returned in duty cycle.

    .. method:: release(index)

        Stop sending a signal to the given servomechanism, releasing it.
