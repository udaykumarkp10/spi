from periphery import SPI

# Open SPI device
spi = SPI("/dev/spidev2.0", 0, 1000000)  # SPI bus 2, device 0, 1 MHz

# Data to send (example data, modify as per your device's protocol)
tx_data = [0x01, 0x02, 0x03, 0x04]

# Send and receive data
rx_data = spi.transfer(tx_data)

# Print received data
print("Received data:", rx_data)

# Close SPI device
spi.close()
