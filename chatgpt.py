import spidev
import time
import math

# ADXL345 Registers
REG_DATAX0 = 0x32
REG_DATAX1 = 0x33
REG_DATAY0 = 0x34
REG_DATAY1 = 0x35
REG_DATAZ0 = 0x36
REG_DATAZ1 = 0x37

# Function to read signed 16-bit value from registers
def read_signed_16bit(data):
    if data[0] & 0x80:
        return -((data[0] ^ 0xFF) << 8 | (data[1] ^ 0xFF)) - 1
    else:
        return (data[0] << 8 | data[1])

# Initialize SPI
spi = spidev.SpiDev()
spi.open(2, 0)  # Open SPI bus 0, device 0

# Function to read accelerometer data
def read_acceleration():
    # Read accelerometer data from registers
    x_raw = read_signed_16bit(spi.xfer2([REG_DATAX0 | 0x80, 0x00]))
    y_raw = read_signed_16bit(spi.xfer2([REG_DATAY0 | 0x80, 0x00]))
    z_raw = read_signed_16bit(spi.xfer2([REG_DATAZ0 | 0x80, 0x00]))

    # Convert raw data to acceleration values (assuming full range)
    # You may need to adjust the sensitivity and scale factors based on your configuration
    scale_factor = 0.004  # Sensitivity scale factor for +/- 2g range (per LSB)
    x_acc = x_raw * scale_factor
    y_acc = y_raw * scale_factor
    z_acc = z_raw * scale_factor

    return x_acc, y_acc, z_acc

def calculate_angle(x_acc, y_acc):
    # Calculate pitch and roll angles
    pitch = math.atan2(x_acc, math.sqrt(y_acc**2 + z_acc**2)) * (180 / math.pi)
    roll = math.atan2(y_acc, math.sqrt(x_acc**2 + z_acc**2)) * (180 / math.pi)

    return pitch, roll

# Main function
def main():
    try:
        while True:
            # Read accelerometer data
            x_acc, y_acc, z_acc = read_acceleration()

            # Calculate pitch and roll angles
            pitch, roll = calculate_angle(x_acc, y_acc)

            # Print angles
            print("Pitch: {:.2f} degrees, Roll: {:.2f} degrees".format(pitch, roll))

            # Wait before the next reading
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Clean up SPI
        spi.close()
        print("Exiting program.")

if __name__ == "__main__":
    main()
