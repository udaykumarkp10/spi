import spidev
import time
import ctypes

# Define byte values
one = ctypes.c_uint8(0x03).value
two = ctypes.c_uint8(0x00).value
three = ctypes.c_uint8(0x50).value
four = ctypes.c_uint8(0xFF).value
five = ctypes.c_uint8(0xFF).value
six = ctypes.c_uint8(0xFF).value
seven = ctypes.c_uint8(0xFF).value


# SPI setup
spi = spidev.SpiDev()
spi.open(2, 0)  # Assuming SPI bus 0, device 0
spi.max_speed_hz = 30000000  # Adjust as needed
spi.mode = 3

# Additional settings
# spi.no_cs = True            # Disable hardware CS
spi.bits_per_word = 8  # Data size is 8 bits (SPI_DATASIZE_8BIT)
spi.cshigh = False  # Use hardware CS
spi.lsbfirst = False  # MSB first (SPI_FIRSTBIT_MSB)
spi.threewire = False  # Use 3-wire mode (SPI_DIRECTION_2LINES)
# spi.loop = False  # Disable loopback mode

while True:
  tx_data = [one, two, three, four, five, six, seven]
  print(len(one))
  # Perform SPI transaction
  rx_data = spi.xfer2(tx_data)
  # Display received data
  print("Received Data:", rx_data)
  time.sleep(0.2)

# Close SPI (not reached in this example)
spi.close()
