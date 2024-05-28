import periphery
import time

# Initialize SPI communication
spi = periphery.SPI("/dev/spidev2.0", mode=0, max_speed=500000)

# Function to perform full-duplex SPI communication
def spi_full_duplex(data_out):
    # Perform full-duplex SPI communication
    data_in = spi.transfer(data_out)
    return data_in

# Example usage
def main():
    # Example data to send
    data_to_send = [0xAA, 0xBB, 0xCC, 0xDD]

    # Perform full-duplex SPI communication
    received_data = spi_full_duplex(data_to_send)

    # Print sent and received data
    print("Sent data:    ", data_to_send)
    print("Received data:", received_data)

if __name__ == "__main__":
    try:
        main()
    finally:
        # Close SPI communication
        spi.close()
