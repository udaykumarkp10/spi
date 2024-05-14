import spidev
import adxl345.base

WRITE_MASK = 0x0
READ_MASK = 0x80
MULTIREAD_MASK = 0x40

class ADXL345(adxl345.base.ADXL345_Base):

    def __init__(self, spi_bus=2, spi_device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(spi_bus, spi_device)
        self.spi.mode = 0b11
        self.spi.max_speed_hz = 5000000
        self.spi.bits_per_word = 8
        self.spi.threewire = False
        self.spi.cshigh = False
        self.spi.lsbfirst = False

    def get_register(self, address):
        value = self.spi.xfer2([address | READ_MASK])
        return value[0]

    def get_registers(self, address, count):
        self.spi.writebytes([address | READ_MASK | MULTIREAD_MASK])
        values = self.spi.readbytes(count)
        return values

    def set_register(self, address, value):
        self.spi.writebytes([address | WRITE_MASK, value])

    def get_axes(self):
        """ return values for the 3 axes of the ADXL, expressed in g (multiple of earth gravity) """
        bytes = self.get_registers(ADXL345_Base.REG_DATAX0, 6)
        x = self._convert(bytes[0], bytes[1])
        y = self._convert(bytes[2], bytes[3])
        z = self._convert(bytes[4], bytes[5])
        return {'x': x,
                'y': y,
                'z': z}


# Example usage
if __name__ == "__main__":
    # Create an instance of the ADXL345 driver
    adxl345 = ADXL345()

    # Read the device ID register (register address 0x00)
    device_id = adxl345.get_register(0x00)

    # Print the device ID
    print("Device ID:", device_id)

    # Read the X, Y, and Z axes
    x, y, z = adxl345.get_axes()

    # Print the readings
    print("X-axis:", x)
    print("Y-axis:", y)
    print("Z-axis:", z)
