from periphery import SPI
import time

# Open SPI device
spi = SPI("/dev/spidev2.0", mode=3, max_speed=3000000)  # SPI bus 2, mode 3, 3 MHz

spi.bits_per_word = 8  # Data size is 8 bits (SPI_DATASIZE_8BIT)
spi.lsbfirst = False  # MSB first (SPI_FIRSTBIT_MSB)
spi.threewire = False  # Use 3-wire mode (SPI_DIRECTION_2LINES)
spi.cshigh = False  # Chip Select active low

def lan9252_read(address, nbytes=7):
    # Prepare the command and address
    command = 0x03  # Read operation
    addr_high = (address >> 8) & 0xFF  # High byte of the address
    addr_low = address & 0xFF  # Low byte of the address
    data_to_send = [command, addr_high, addr_low] + [0] * nbytes

    # Perform SPI transfer
    rx_data = spi.transfer(data_to_send)

    # The first three bytes are the command and address bytes, followed by the response data
    return rx_data[3:]  # Skip the first three bytes

def main():
    while True:
        # Read 7 bytes from register 0x0064
        address = 0x0064
        received_data = lan9252_read(address)

        # Print the received data in hexadecimal format
        hex_data = ' '.join(f'0x{byte:02X}' for byte in received_data)
        print("Received Data:", hex_data)
        # Wait for 1 second
        time.sleep(1)

if __name__ == "__main__":
    main()

# Close SPI connection when done
spi.close()
