import spidev
import time
import ctypes

# Configuration constants
SPI_BUS = 2
SPI_DEVICE = 0
SPI_MAX_SPEED_HZ = 50000

# EtherCAT command constants
ESC_CMD_READ = 0x02
ESC_CMD_WRITE = 0x04

# Define the EtherCAT IOmap
IOmap = (ctypes.c_uint8 * 4096)()

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

def write_register(register, data):
    command = [ESC_CMD_WRITE, (register >> 8) & 0xFF, register & 0xFF] + data
    spi_transfer(command)

def init_lan9252():
    # Example: Reset the LAN9252
    write_register(0x1F80, [0x00, 0x01])  # Write reset command
    time.sleep(0.1)
    
    # Example: Check for successful reset
    status = read_register(0x1F80, 2)
    if status == [0x00, 0x00]:
        print("LAN9252 reset successfully.")
    else:
        print("Failed to reset LAN9252.")

def main():
    print("Initializing LAN9252...")
    init_lan9252()

    print("Configuring EtherCAT slave...")
    # Example: Configure the EtherCAT slave
    # You will need to adjust this part based on your specific configuration and requirements
    write_register(0x1E00, [0x01, 0x00])  # Example configuration
    time.sleep(0.1)

    print("Starting EtherCAT communication...")
    while True:
        try:
            # Example: Read input data
            inputs = read_register(0x1000, 4)
            print(f"Inputs: {inputs}")

            # Example: Write output data
            outputs = [0x00, 0x01, 0x02, 0x03]
            write_register(0x1400, outputs)
            print(f"Outputs: {outputs}")

            time.sleep(1)
        except KeyboardInterrupt:
            break

    spi.close()
    print("EtherCAT communication stopped.")

if __name__ == "__main__":
    main()
