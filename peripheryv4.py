from periphery import SPI
import time
import ctypes

# Open SPI device
spi = SPI("/dev/spidev2.0", 3, 1000000)  # SPI bus 2, device 0, 1 MHz

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

while True:
  #reset
  tx = [reset_one, reset_two, reset_three, reset_four, reset_five, reset_six, reset_seven]
  print("Number of bytes sent:", len(tx))
  rx_data = spi.transfer(tx)

  print("Received Data:", rx_data)

  """ 
  #byte test
  tx_data = [one, two, three, four, five, six, seven]
  print("Number of bytes sent:", len(tx_data))
  # Perform SPI transaction
  rx_data = spi.transfer(tx_data)
  # Display received data
  print("Received Data:", rx_data)

  """
  
  time.sleep(0.2)

# Close SPI (not reached in this example)
spi.close()
