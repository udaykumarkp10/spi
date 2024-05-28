import periphery
import time

# Initialize SPI communication
spi = periphery.SPI("/dev/spidev2.0", mode=0, max_speed=500000)

# Function to send data over SPI
def spi_send(data):
    spi.transfer(data)

# Function to receive data over SPI
def spi_receive(length):
    return spi.transfer([0x00] * length)

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
