********************************
I2CTarget-Based Motor Controller
********************************

Background
**********

This is an offshoot of two projects: an earlier
`Brushless Motor Controller <https://github.com/ifurusato/brushless-motor-controller>`_.
and a current `KRZOS <https://github.com/ifurusato/krzos>`_ (robot operating system)
project.

Brushless Motor Controller tried various approaches to connecting four DC brushless
motors to a Raspberry Pi, the last and most-developed connecting to an STM32H723
over a UART. While functional, the UART presented a number of serious issues and was
eventually abandoned.

Following a subsequent release of the
`I2CTarget <https://docs.micropython.org/en/latest/library/machine.I2CTarget.html>`_
implementation for MicroPython, this now represents yet another attempt at a much
higher performance and significantly simpler ("dumb") motor controller, connected
over I2C.

While the implementation is suited as a motor controller, with relatively minor
changes it could conceivably be used for any type of exchange of payload data
between a Raspberry Pi master and microcontroller-based slave over I2C.


Functional Description
**********************

This uses a Raspberry Pi master controller, connected via I2C to two pins of an
STM32. The `i2c_master_test.py` test script is used to send a serialised Payload
object to the I2C slave, whose `main.py` file executes an `i2c_slave.py` slave
controller with a `motor_controller.py`, responding in like kind with a serialised
Payload.

The motor controller found herein is just a shell and would be fleshed out with an
dependent upon the specific hardware used.

The test script runs in two modes, one that simply runs through a series of
commands, the other uses a Pimoroni I2C-based digital potentiometer to tune the
master's delay time (which can be somewhat critical in stability of the transactions).

If you don't use the delay tuning mode you won't need the digital potentiometer.

The implementation includes an admittedly large number of ancillary files, both on
the CPython and MicroPython side. This includes custom logging, YAML-based configuration,
and components of the core infrastructure as used in the projects this is targeted
at using. The core of this project may be found in the following files::

    i2c_master_test.py        the test script, including the I2C master implementation
    upy/main.py               the MicroPython main driver
    upy/i2c_slave.py          the I2C slave implementation
    upy/payload.py            the Payload container
    upy/crc8_table.py         a CRC8 checksum support file for Payload
    upy/motor_controller.py   the shell of a motor controller
    upy/command.py            a pseudo-enum providing the set of commands
    upy/response.py           a pseudo-enum used for a response code

The rest are essentially support files, which could be refactored out of the project
if you didn't want YAML configuration, logging, etc.


Performance
***********

Test performance using a Pi Zero 2 W and a 168MHz WeAct STM32F405 has typically
been around 1-2ms for a round trip (send payload, receive payload), with the I2C
bus frequency set at 400KHz.

A higher performance Raspberry Pi with a 1MHz I2C bus frequency and a faster
microcontroller would provide even higher performance. The STM32 used previously
with the Brushless Motor Controller was a 550MHz WeAct STM32H723, and this will
be used for the final implementation.

Conceivably any device capable of serving as I2C master and any microcontroller
supported by I2CTarget could be used.


Requirements
************

This library requires Python 3.8.5 or newer. It's currently being written using
Python 3.11.2. Some portions (modules) of the code will only run on a Raspberry
Pi, though KRZOS Core should function independently of the various Pi
libraries.

KRZOS requires installation of a number of dependencies (support libraries).
There is currently no dependency management set up for this project.

First::

  sudo apt install python3-pip

then:

* colorama:     https://pypi.org/project/colorama/
    with:         sudo apt install python3-colorama
* pyyaml:       https://pypi.org/project/PyYAML/
    with:         sudo apt install python3-yaml
* smbus2      : https://pypi.org/project/smbus2/
    with:         sudo apt install python3-smbus2

The Micropython files are found in the ./upy/ directory.


Getting Started
***************

Once the requirements are met, either do a hard reset on the microcontroller
or execute main.py from the REPL to start the slave, which must be running
prior to starting the master. Execute i2c_master_test.py on the Pi, which will
run through its paces depending on its set mode. If you set `DELAY_TUNING_TEST`
True and have a digital potentiometer connected, altering its value will change
both the transaction delay time (which defaults to 700µS) as well as the motor
speed sent to the motor controller


Status
******

The project is functional, though hardly finished. It is still under active
development and should not be considered stable.

* 2025-10-23: initial checkin, a copy from the krzos project


Support & Liability
*******************

This project comes with no promise of support or acceptance of liability. Use at
your own risk.


Copyright & License
*******************

All contents (including software, documentation and images) Copyright 2020-2025
by Murray Altheim. All rights reserved.

Software and documentation are distributed under the MIT License, see LICENSE
file included with project.

