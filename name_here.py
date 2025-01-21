#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2020 Greg Davill <greg.davill@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.lattice import LatticeECP5Platform
from litex.build.dfu import DFUProg

#the goal is that the naming conventions will match with the schematic

# IOs ----------------------------------------------------------------------------------------------

_io_r0_1 = [ # revision, could have a _io_r0_2 if for some reason we had a seperate revision of the board
    # Rst
    ("fpga_reset", 0, Pins("R9"), IOStandard("LVCMOS33")),


    # Define the pins for the SPI fram interface
    ("fram", 0,
        Subsignal("cs", Pins("R6"), IOStandard("LVCMOS33")), #chip select
        Subsignal("so",   Pins("R7"), IOStandard("LVCMOS33")),  # Serial Out (MISO)
        Subsignal("hold",  Pins("P7"), IOStandard("LVCMOS33")),  # Hold
        Subsignal("sck",  Pins("T7"), IOStandard("LVCMOS33")),  # serial clock
        Subsignal("si",  Pins("T6"), IOStandard("LVCMOS33")) # serial in
        
    ),

    #define the pins for SRAM
    ("ram", 0,
        #address pins A0-A17
        Subsignal("a", Pins("M13 M14 M15 K13 K14 J12 J13 J14 E16 E15 F16 F15 F14 E13 F13 H14 H13 G13"), IOStandard("LVCMOS33")),
        
        # Data pins I/O0 to I/O15
        Subsignal("io",   Pins("L15 L16 K15 K16 J15 H15 J16 G15 L13 G12 K12 H12 F12 E12 G14 D13"), IOStandard("LVCMOS33")),  
        
        Subsignal("ce",  Pins("M16"), IOStandard("LVCMOS33")),  # chip enable
        Subsignal("oe",  Pins("L12"), IOStandard("LVCMOS33")),  # output enable
        Subsignal("we",  Pins("G5"), IOStandard("LVCMOS33")), # write enable
        Subsignal("lb",  Pins("A1"), IOStandard("LVCMOS33")), # lower byte
        Subsignal("ub",  Pins("B2"), IOStandard("LVCMOS33")) # upper byte
    ),


    # USB Data
    ("usb", 0,
        Subsignal("d_p", Pins("B1")),
        Subsignal("d_n", Pins("B2")),
        Subsignal("pullup", Pins("C2")),
        IOStandard("LVCMOS33")
    ),

    # 5V tolerant I/O
    ("tolerant_IO", 0,
        Subsignal("a", Pins("A13 B14 A14 B15 C15 B16 C16 D16")),
        Subsignal("oe", Pins("C13")),
        Subsignal("b", Pins("A13_i B14_i A14_i B15_i C15_i B16_i C16_i D16_i")),
        IOStandard("LVCMOS33")

    ),

    clk
    ("clk", 0,
        # Input/Output pins for the clock generator
        Subsignal("y3",    Pins("C8"), IOStandard("LVCMOS33")),  # Output signal Y3
        Subsignal("y1",    Pins("J1"), IOStandard("LVCMOS33")),  # Output signal Y1
        Subsignal("y2",    Pins("K1"), IOStandard("LVCMOS33"))  # Output signal Y2
    ),

    #FTDI
    ("FTDI", 0,
        Subsignal("tdo", Pins("M10"), IOStandard("LVCMOS33")),
        Subsignal("tck", Pins("T10"), IOStandard("LVCMOS33")),
        Subsignal("tdi", Pins("R11"), IOStandard("LVCMOS33")),
        Subsignal("tms", Pins("T11"), IOStandard("LVCMOS33")),
        Subsignal("d_n", Pins("B2"), IOStandard("LVCMOS33")),
        Subsignal("d_p", Pins("B1"), IOStandard("LVCMOS33"))

    ),

     #QSPI Flash
    ("QSPI", 0,
        Subsignal("cs", Pins("N8"), IOStandard("LVCMOS33")),
        Subsignal("MISO", Pins("T7"), IOStandard("LVCMOS33")),
        Subsignal("d2", Pins("M7"), IOStandard("LVCMOS33")),
        Subsignal("d3", Pins("N7"), IOStandard("LVCMOS33")),
        Subsignal("sck", Pins("N9"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("T8"), IOStandard("LVCMOS33"))
        
    )

    # I2C Interface for MS5351M
    ("i2c", 0,
        Subsignal("scl", Pins("C4")),  # Clock line (I2C SCL)
        Subsignal("sda", Pins("D5")),  # Data line (I2C SDA)
        IOStandard("LVCMOS33")
    ),
    
]



# Connectors ---------------------------------------------------------------------------------------

_connector_r0_1 = [
     #connector 1
    ("gpio_1", Pins("E3 C1 E2 D1 F2 E1 G2 F1 H2 G1 F3 P1 R1 T2 T3 K2 L2 N1 P2 M3 P3 N3") IOStandard("LVCMOS33")),
    #connector 2
    ("gpio_2", Pins("R4 T4 P4 N5 M5 N11 R12 P12 R13 T13 P13 R15 P14 N12 T14 R14 T15 R16 P15 P16 N14 N16") IOStandard("LVCMOS33")),
    #connector 3
    ("gpio_3", Pins("D3 C3 B3 A3 B4 A4 B5 A5 B6 A6 B7 D6 C5 D7 C6 C7 B8 C9 D9 B9 C10 D11") IOStandard("LVCMOS33")),
    #connector 4
    ("gpio_4", Pins("A8 B10 A9 C11 A10 B12 A11 B11 A12 B13 C12 C14 D14 E14 A13_i B14_i A14_i B15_i C15_i B16_i C16_i D16_i") IOStandard("LVCMOS33"))

    
]



# Platform -----------------------------------------------------------------------------------------

class Platform(LatticeECP5Platform):
    # LFE5U-25F-6BG256C
    default_clk_name   = "clk"
    default_clk_period = 1e9 / 27e6  # 27 MHz clock

    def __init__(self, device="25F", toolchain="trellis", **kwargs):
        # Initialize the platform with the Lattice ECP5 device (adjust with your specific board)
        LatticeECP5Platform.__init__(self, f"LFE5U-{device}-6BG256C", _io_r0_1, _connector_r0_1, toolchain=toolchain, **kwargs)
        self.i2c = I2CController(self)

    def create_programmer(self):
        # Create a DFU programmer for flashing the FPGA (adjust as needed)
        return DFUProg(vid="1209", pid="5af0", alt=0)

    def do_finalize(self, fragment):
        # Perform final steps like adding constraints
        LatticeECP5Platform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk", loose=True), 1e9 / 48e6)  # 48 MHz clock (example constraint)
