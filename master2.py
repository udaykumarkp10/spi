import spidev
import time

while True:
    spi = spidev.SpiDev()
    spi.open(2, 0)  # Assuming SPI bus 2, device 0

    spi.mode = 0b00
    spi.lsbfirst = False

    # Setting speed to 1000Hz
    spi.max_speed_hz = 1000

    # Set measurement mode

    data = 0xAA
    spi.xfer([data])  # Pass data as a list

    spi.close()

    # Wait for some time before sending next data
    time.sleep(1)
