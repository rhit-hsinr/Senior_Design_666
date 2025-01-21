from litex.soc.cores.i2c import I2CController
from litex.soc.integration import csr_core
from litex.soc.cores.clock import ClockDomain
from migen import *

# MS5351M-specific I2C register addresses and bit settings (example)
MS5351M_ADDR = 0x60  # I2C address of MS5351M (check datasheet for exact value)
MS5351M_REG_CONFIG = 0x00  # Configuration register (example address)
MS5351M_REG_FREQUENCY = 0x01  # Frequency register (example address)

class ClockGenerator(Module, csr_core.CSRStatus, csr_core.CSRControl):
    def __init__(self, platform, clk_freq=27e6):
        self.platform = platform
        self.i2c = I2CController(platform)
        
        # Clock output pins (y1, y2, y3) - connected in platform file
        self.clk_y1 = self.platform.request("clk", 0)
        self.clk_y2 = self.platform.request("clk", 1)
        self.clk_y3 = self.platform.request("clk", 2)
        
        # Frequency selection control (example - adjust as necessary)
        self.selected_frequency = Signal(2)  # Select between 3 frequencies (2 bits)
        
        # I2C to communicate with the MS5351M
        self.configure_clock_generator()
        
        # Add clock domain for SoC clock
        self.submodules.crg = ClockDomain()

    def configure_clock_generator(self):
        # Reset the clock generator (if necessary)
        self.i2c.write(MS5351M_ADDR, MS5351M_REG_CONFIG, 0x00)  # Example reset
        
        # Set initial frequency (as an example)
        self.set_frequency(27e6)  # Set to default frequency of 27 MHz
        
    def set_frequency(self, frequency):
        # Convert frequency to the correct register format (depends on MS5351M datasheet)
        # Example: Assuming you send the frequency as a register value
        register_value = self.calculate_register_value(frequency)
        self.i2c.write(MS5351M_ADDR, MS5351M_REG_FREQUENCY, register_value)

    def calculate_register_value(self, frequency):
        # Convert frequency to register value based on the MS5351M datasheet formula
        # This is a placeholder calculation and needs to be replaced by actual formula
        return int(frequency * 1000)  # Example conversion (adjust as needed)
    
    def select_output_frequency(self, freq_idx):
        # Select which output to use (y1, y2, y3) based on the selected frequency
        if freq_idx == 0:
            self.selected_frequency = 0
            # Update I2C registers or use logic to select y1
        elif freq_idx == 1:
            self.selected_frequency = 1
            # Update I2C registers or use logic to select y2
        elif freq_idx == 2:
            self.selected_frequency = 2
            # Update I2C registers or use logic to select y3

        # More logic for actual frequency setting could be added here