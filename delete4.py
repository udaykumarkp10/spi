import spidev
import time

# Configuration constants
SPI_BUS = 2
SPI_DEVICE = 0
SPI_MAX_SPEED_HZ = 50000

# EtherCAT command constants
ESC_CMD_READ = 0x03

# Initialize the SPI interface
spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = SPI_MAX_SPEED_HZ
spi.mode = 0b11

def spi_transfer(data):
    response = spi.xfer2(data)
    return response

def read_register(register, length):
    command = [ESC_CMD_READ, (register >> 8) & 0xFF, register & 0xFF] + [0] * length
    response = spi_transfer(command)
    return response[3:]

def main():
    print("Reading from register 0x0064...")
    while True:
        try:
            # Read input data from register address 0x0064
            inputs = read_register(0x0064, 4)
            print(f"Inputs from register 0x0064: {inputs}")

            time.sleep(1)
        except KeyboardInterrupt:
            break

    spi.close()
    print("SPI communication stopped.")

if __name__ == "__main__":
    main()
