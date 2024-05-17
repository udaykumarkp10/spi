import time
from periphery import SPI

# Open SPI device
spi = SPI("/dev/spidev2.0", 0, 1000000)  # SPI bus 2, device 0, 1 MHz

# Data to send (example data, modify as per your device's protocol)
tx_data = [0x01, 0x02, 0x03, 0x04]

try:
    while True:
        # Send and receive data
        rx_data = spi.transfer(tx_data)

        # Print received data
        print("Received data:", rx_data)

        # Delay for 0.1 seconds
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Ctrl+C detected. Exiting gracefully.")

finally:
    # Close SPI device
    spi.close()
