from periphery import SPI
import time

# Open SPI device
spi = SPI("/dev/spidev2.0", mode=3, max_speed=5000000)  # SPI bus 2, mode 3, 5 MHz

# Functions
def adxl_write(address, value):
    data = [address & 0x3F, value]
    spi.transfer(data)  # Transmit the address and data

def adxl_read(address, nbytes=1):
    address |= 0x80  # Read operation
    address |= 0x40  # Multibyte read
    rx_data = spi.transfer([address] + [0]*nbytes)
    return rx_data[1:] if nbytes > 1 else rx_data[0]

def adxl_init():
    adxl_write(0x31, 0x01)  # data_format range= +- 4g
    adxl_write(0x2d, 0x00)  # reset all bits
    adxl_write(0x2d, 0x08)  # power_cntl measure and wake up 8Hz

# Main function
def main():
    adxl_init()  # Initialize ADXL345

    # Read device ID
    device_id = adxl_read(0x00)

    print("ADXL345 Device ID:", hex(device_id))

    while True:
        # Read data
        data_rec = adxl_read(0x32, nbytes=6)
        x = (data_rec[1] << 8) | data_rec[0]
        y = (data_rec[3] << 8) | data_rec[2]
        z = (data_rec[5] << 8) | data_rec[4]

        # Convert into 'g'
        xg = x * 0.0078
        yg = y * 0.0078
        zg = z * 0.0078

        # Display the result (print to console)
        print("X: %.5f g, Y: %.5f g, Z: %.5f g" % (xg, yg, zg))

        # Wait for 1 second
        time.sleep(2)

if __name__ == "__main__":
    main()
