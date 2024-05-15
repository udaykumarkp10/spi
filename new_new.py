import spidev
import time
import ctypes


# Define byte values
reset_one = ctypes.c_uint8(0x02).value
reset_two = ctypes.c_uint8(0x01).value
reset_three = ctypes.c_uint8(0xF8).value
reset_four = ctypes.c_uint8(0x00).value
reset_five = ctypes.c_uint8(0x00).value
reset_six = ctypes.c_uint8(0x00).value
reset_seven = ctypes.c_uint8(0x00).value


# Define byte values
one = ctypes.c_uint8(0x03).value
two = ctypes.c_uint8(0x00).value
three = ctypes.c_uint8(0x64).value
four = ctypes.c_uint8(0xFF).value
five = ctypes.c_uint8(0xFF).value
six = ctypes.c_uint8(0xFF).value
seven = ctypes.c_uint8(0xFF).value


# SPI setup
spi = spidev.SpiDev()
spi.open(2, 0)  # Assuming SPI bus 0, device 0
spi.mode = 3
spi.bits_per_word = 8  # Data size is 8 bits (SPI_DATASIZE_8BIT)
spi.lsbfirst = False  # MSB first (SPI_FIRSTBIT_MSB)
spi.threewire = False  # Use 3-wire mode (SPI_DIRECTION_2LINES)

"""

spi.max_speed_hz = 30000000  # Adjust as needed
spi.mode = 3

# Additional settings
# spi.no_cs = True            # Disable hardware CS
spi.bits_per_word = 8  # Data size is 8 bits (SPI_DATASIZE_8BIT)
spi.cshigh = False  # Use hardware CS
spi.lsbfirst = False  # MSB first (SPI_FIRSTBIT_MSB)
spi.threewire = False  # Use 3-wire mode (SPI_DIRECTION_2LINES)
# spi.loop = False  # Disable loopback mode

"""

while True:
  #reset
  tx = [reset_one, reset_two, reset_three, reset_four, reset_five, reset_six, reset_seven]
  print("Number of bytes sent:", len(tx))
  rx = spi.xfer2(tx)
  print("Received Data:", rx)

  #byte test
  tx_data = [one, two, three, four, five, six, seven]
  print("Number of bytes sent:", len(tx_data))
  # Perform SPI transaction
  rx_data = spi.xfer2(tx_data)
  # Display received data
  print("Received Data:", rx_data)
  time.sleep(0.2)

# Close SPI (not reached in this example)
spi.close()
