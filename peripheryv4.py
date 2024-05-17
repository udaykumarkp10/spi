from periphery import SPI

# Open SPI device
spi = SPI("/dev/spidev2.0", 0, 1000000)  # SPI bus 2, device 0, 1 MHz
