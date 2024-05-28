import periphery
import time

# Initialize SPI communication
spi = periphery.SPI("/dev/spidev2.0")

# Set SPI parameters (optional)
spi.frequency = 500000  # Set SPI frequency (max speed depends on your hardware and SD card)
spi.mode = 0            # Set SPI mode (0, 1, 2, or 3)
spi.bits_per_word = 8  # Set number of bits per word

# Function to send data over SPI
def spi_send(data):
    spi.write(data)

# Function to receive data over SPI
def spi_receive(length):
    return spi.read(length)

# Example usage
def main():
    # Example data to send
    data_to_send = [0xAA, 0xBB, 0xCC, 0xDD]

    # Send data
    spi_send(data_to_send)

    # Receive data (assuming we want to receive the same number of bytes as sent)
    received_data = spi_receive(len(data_to_send))
    print("Received data:", received_data)

if __name__ == "__main__":
    try:
        main()
    finally:
        # Close SPI communication
        spi.close()
