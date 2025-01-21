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
