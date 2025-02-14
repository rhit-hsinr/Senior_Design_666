from litex.soc.integration.soc import SoC
from litex.soc.integration.builder import Builder
import time

# Request GPIO pins from the platform (assumes LCD is connected via a GPIO connector)
lcd_io = platform.request("gpio_2")

rs, rw, e = lcd_io[0], lcd_io[1], lcd_io[2]
d4, d5, d6, d7 = lcd_io[3], lcd_io[4], lcd_io[5], lcd_io[6]

def pulse_enable():
    e.eq(1)
    time.sleep(0.000001)
    e.eq(0)
    time.sleep(0.000001)

def lcd_write_4bits(data):
    d4.eq((data >> 0) & 1)
    d5.eq((data >> 1) & 1)
    d6.eq((data >> 2) & 1)
    d7.eq((data >> 3) & 1)
    pulse_enable()

def lcd_command(cmd):
    rs.eq(0)
    lcd_write_4bits(cmd >> 4)
    lcd_write_4bits(cmd & 0x0F)

def lcd_data(data):
    rs.eq(1)
    lcd_write_4bits(data >> 4)
    lcd_write_4bits(data & 0x0F)

def lcd_init():
    time.sleep(0.05)
    lcd_write_4bits(0x03)
    time.sleep(0.005)
    lcd_write_4bits(0x03)
    time.sleep(0.0001)
    lcd_write_4bits(0x03)
    lcd_write_4bits(0x02)
    
    lcd_command(0x28)
    lcd_command(0x0C)
    lcd_command(0x06)
    lcd_command(0x01)
    time.sleep(0.002)

def lcd_print(text):
    for char in text:
        lcd_data(ord(char))

# Main Program
lcd_init()
lcd_print("Hello, LiteX!")
