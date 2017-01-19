from distutils.core import setup


setup(
    name='adafruit-pca9685',
    packages=[
        'adafruit_pca9685',
    ],\
    version="2.0.0",
    description="Driver for PCA9685 for Adafruit CircuitPython.",
    long_description="""\
This library lets you control the motor, stepper, and servo drivers based on PCA9685.""",
    author='Radomir Dopieralski & Adafruit Industries',
    author_email='support@adafruit.com',
    classifiers = [
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    url="https://github.com/adafruit/Adafruit_CircuitPython_PCA9685"
)
