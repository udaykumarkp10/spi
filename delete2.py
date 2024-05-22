from periphery import SPI
import time

# Open SPI device
spi = SPI("/dev/spidev2.0", mode=3, max_speed=5000000)  # SPI bus 2, mode 3, 5 MHz

# SPI configuration
spi.bits_per_word = 8  # Data size is 8 bits (SPI_DATASIZE_8BIT)
spi.lsbfirst = False  # MSB first (SPI_FIRSTBIT_MSB)
spi.threewire = False  # Use 3-wire mode (SPI_DIRECTION_2LINES)
spi.cshigh = False  # Chip Select active low

def device_read(command, address, nbytes=7):
    # Prepare the command and address
    data_to_send = [command, address] + [0xFF] * nbytes  # Use 0xFF as dummy data for reading

    # Perform SPI transfer
    rx_data = spi.transfer(data_to_send)

    # The first two bytes are the command and address bytes, followed by the response data
    return rx_data[2:]  # Skip the first two bytes

def main():
    command = 0x03  # Read command
    address = 0x64  # 8-bit address to read from

    while True:
        # Read 7 bytes from the specified address
        received_data = device_read(command, address)

        # Print the received data in hexadecimal format
        hex_data = ' '.join(f'0x{byte:02X}' for byte in received_data)
        print("Received Data:", hex_data)
        
        # Wait for 1 second
        time.sleep(1)

if __name__ == "__main__":
    main()

# Close SPI connection when done
spi.close()
