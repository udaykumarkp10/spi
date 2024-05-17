from periphery import SPI

# Open SPI device
spi = SPI("/dev/spidev2.0", mode=3, max_speed=5000000)  # SPI bus 2, mode 3, 5 MHz

# Function to read device ID
def read_device_id():
    # Send read command for device ID (register address 0x00)
    rx_data = spi.transfer([0x00 | 0x80, 0x00])
    # Extract device ID from received data
    device_id = rx_data[1]
    return device_id

# Main function
def main():
    # Read device ID
    device_id = read_device_id()

    print("ADXL345 Device ID:", hex(device_id))

if __name__ == "__main__":
    main()
