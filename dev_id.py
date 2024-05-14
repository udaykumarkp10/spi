import spidev
import time

WRITE_MASK = 0x0
READ_MASK = 0x03
MULTIREAD_MASK = 0x40

# Define custom command code
READ_COMMAND = 0x03  # Read command

# SPI setup
spi = spidev.SpiDev()
spi.open(2, 0)  # Assuming SPI bus 0, device 0
spi.max_speed_hz = 30000000
spi.mode = 0b11

# Additional settings
spi.bits_per_word = 8  # Data size is 8 bits (SPI_DATASIZE_8BIT)
spi.cshigh = False  # Use hardware CS
spi.lsbfirst = False  # MSB first (SPI_FIRSTBIT_MSB)
spi.threewire = False  # Use 3-wire mode (SPI_DIRECTION_2LINES)


def spi_read_byte_test():
    # Prepare command and address
    tx_data = [READ_COMMAND, 0x87, 0x65, 0x43, 0x21]

    # Perform SPI transfer
    rx_data = spi.xfer2(tx_data)

    # Process received data
    result = (rx_data[1] << 24) | (rx_data[2] << 16) | (rx_data[3] << 8) | rx_data[4]

    return result

# Example usage
if __name__ == "__main__":
    byte_test_value = spi_read_byte_test()
    print("Byte Test value:", hex(byte_test_value))

# Cleanup SPI
spi.close()

