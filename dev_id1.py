import spidev
import time

WRITE_MASK = 0x0
READ_MASK = 0x03
MULTIREAD_MASK = 0x40

ID_REV = 0x0050

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

def spi_transfer(data):
    # Perform SPI transfer
    rx_data = spi.readbytes(len(data))
    return rx_data

# Example usage
if __name__ == "__main__":
    while(True):
        data_to_send = [0x03, 0x00, 0x50, 0xFF, 0xFF, 0xFF, 0xFF]

        # Perform SPI transfer
        received_data = spi_transfer(data_to_send)
        print("Received data:", received_data)
        time.sleep(0.2)
