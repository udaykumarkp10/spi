import spidev
import time
import ctypes

# Define byte values
one = ctypes.c_uint8(0x03).value
two = ctypes.c_uint8(0x00).value
three = ctypes.c_uint8(0x64).value
four = ctypes.c_uint8(0xFF).value
five = ctypes.c_uint8(0xFF).value
six = ctypes.c_uint8(0xFF).value
seven = ctypes.c_uint8(0xFF).value

# Initialize SPI
spi = spidev.SpiDev()
spi.open(2, 0)  # Open SPI bus 2, device 0
spi.max_speed_hz = 30000000  # Set SPI speed to 30 MHz
spi.mode = 0b11

counter = 0
while True:
  tx_data = [one, two, three, four, five, six, seven]
  # Perform SPI transaction
  rx_data = spi.xfer2(tx_data)
  # Display received data
  print("Received Data:", rx_data)
  time.sleep(0.2)

# Close SPI (not reached in this example)
spi.close()
