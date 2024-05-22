from periphery import SPI
import time

# Open SPI device
spi = SPI("/dev/spidev2.0", mode=3, max_speed=3000000)  # SPI bus 2, mode 3, 3 MHz

# SPI configuration
spi.bits_per_word = 8  # Data size is 8 bits
spi.lsbfirst = False   # MSB first
spi.threewire = False  # Use 3-wire mode
spi.cshigh = False     # Chip Select active low

def device_read(address, nbytes=7):
    # Prepare the command and address for read operation
    address |= 0x80  # Set the read bit (bit 7)
    if nbytes > 1:
        address |= 0x40  # Multibyte read (set bit 6)
    
    # Transmit the address and read nbytes of data
    tx_data = [address] + [0xFF] * nbytes
    rx_data = spi.transfer(tx_data)
    
    # Return received data (skip the address byte)
    return rx_data[1:]

def main():
    address = 0x64  # 8-bit address to read from

    try:
        while True:
            # Read 7 bytes from the specified address
            received_data = device_read(address)

            # Print the received data in hexadecimal format
            hex_data = ' '.join(f'0x{byte:02X}' for byte in received_data)
            print("Received Data:", hex_data)
            
            # Wait for 1 second
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        # Close SPI connection when done
        spi.close()

if __name__ == "__main__":
    main()
