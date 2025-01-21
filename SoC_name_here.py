#!/usr/bin/env python3

#
# This file is part of LiteX-Boards.
#
# Copyright (c) Greg Davill <greg.davill@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

import os
import sys

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex.gen import *
from litex.gen.genlib.misc import WaitTimer

from litex_boards.platforms import gsd_orangecrab

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.led import LedChaser

from litex.soc.integration.soc import SoC
from litex.soc.cores.spi import QuadSPI
from litex.soc.cores.memory import SRAM
from litex.soc.cores.usb import USB
from litex.soc.cores.gpio import GPIOIn, GPIOOut
from litex.soc.cores.clock import ClockDomain
from litex.soc.integration.platform import Platform

from clock_generator import ClockGenerator

class MS5351MClockGenerator(Module):
    def __init__(self, platform, i2c_bus, slave_address=0x60):
        """
        MS5351M Clock Generator Class to interface with the MS5351M over I2C.

        Args:
            platform: The LiteX platform that the clock generator is attached to.
            i2c_bus: The I2C bus object to communicate with the MS5351M.
            slave_address: The I2C address of the MS5351M (default: 0x60).
        """
        self.i2c = I2C(platform, i2c_bus)
        self.slave_address = slave_address

        # Output clock frequencies (in Hz)
        self.output_frequencies = [0, 0, 0]  # Three output frequencies initialized to 0
        self.setup_clock_generator()

    def setup_clock_generator(self):
        """
        Initializes the MS5351M clock generator with default settings.
        Configures the MS5351M outputs.
        """
        # Reset the MS5351M (write 0 to reset register)
        self._write_register(0x00, 0x01)  # Assuming 0x00 is the reset register

        # Setup default frequencies (can be adjusted later)
        self.set_frequency(0, 50e6)  # Set output 1 to 50 MHz (example)
        self.set_frequency(1, 100e6)  # Set output 2 to 100 MHz (example)
        self.set_frequency(2, 200e6)  # Set output 3 to 200 MHz (example)

    def set_frequency(self, output_index, frequency):
        """
        Set the frequency of a specific output (0, 1, or 2).

        Args:
            output_index: The output index (0, 1, or 2).
            frequency: The desired frequency in Hz.
        """
        if output_index not in [0, 1, 2]:
            raise ValueError("Invalid output index. Must be 0, 1, or 2.")

        # Calculate the register value based on the frequency
        register_value = self._calculate_register_value(frequency)
        
        # Write the register value to the correct output register
        register_address = 0x10 + output_index * 2  # Assuming output registers start at 0x10
        self._write_register(register_address, register_value)

        # Update the output frequency
        self.output_frequencies[output_index] = frequency

    def _calculate_register_value(self, frequency):
        """
        Calculate the register value to set the output frequency.

        Args:
            frequency: The desired frequency in Hz.

        Returns:
            The calculated register value.
        """
        # This function will need to convert the frequency to the appropriate register value.
        # Assuming MS5351M uses a direct calculation method for frequency:
        # This is a placeholder calculation. Refer to the MS5351M datasheet for the exact formula.
        
        # For example, assuming frequency to register value is direct:
        register_value = int(frequency / 1e6)  # Example conversion to MHz

        return register_value

    def _write_register(self, register, value):
        """
        Write a value to a specific register via I2C.

        Args:
            register: The register address.
            value: The value to write to the register.
        """
        data = [register, value & 0xFF, (value >> 8) & 0xFF]  # Assuming 16-bit registers
        self.i2c.write(self.slave_address, data)
        time.sleep(0.01)  # Short delay to ensure register is written


class BaseSoC(BaseSoC):
    def __init__(self, platform, sys_clk_freq=int(27e6), with_fram=False, **kwargs):
        # SoC constructor
        BaseSoC.__init__(self, platform, clk_freq=sys_clk_freq, **kwargs)

        # FRAM (optional)
        if with_fram:
            self.fram = FRAM(platform, size=32 * 1024 * 1024)  # example 32 MB size
            self.add_memory_region("fram", self.fram.bus.base, 32 * 1024 * 1024)
            self.add_wb_slave(self.fram.bus.base, self.fram.bus)

        # SRAM
        self.sram = SRAM(platform, size=256 * 1024)  # 256 KB SRAM
        self.add_memory_region("sram", self.sram.bus.base, 256 * 1024)
        self.add_wb_slave(self.sram.bus.base, self.sram.bus)

        # GPIO Example (connected to platform's gpio_1 pinout)
        self.gpio_1 = GPIOOut(platform, pins="gpio_1")
        self.gpio_2 = GPIOOut(platform, pins="gpio_2")
        self.gpio_3 = GPIOOut(platform, pins="gpio_3")
        self.gpio_4 = GPIOOut(platform, pins="gpio_4")
        self.add_csr("gpio_1")
        self.add_csr("gpio_2")
        self.add_csr("gpio_3")
        self.add_csr("gpio_4")

        # USB (optional)
        self.usb = USB(platform)
        self.add_csr("usb")

        # FTDI (optional)
        self.ftdi = FTDI(platform)
        self.add_csr("ftdi")

        # QSPI Flash (optional)
        self.qspi = QSPI(platform)
        self.add_csr("qspi")

        # I2C Bus for clock generator (assuming I2C is available on the platform)
        self.i2c_bus = platform.request("i2c")

        # Clock Generator (MS5351M)
        self.clock_generator = ClockGenerator(platform)
        self.add_csr("clock_generator")

# Build the platform and SoC
platform = Platform()
soc = BaseSoC(platform, sys_clk_freq=27e6, with_fram=True)
platform.build(soc)
