import spidev
import time

# Registers
REG_DEVICE_ID = 0x00
REG_THRESH_TAP = 0x1D
REG_OFSX = 0x1E
REG_OFSY = 0x1F
REG_OFSZ = 0x20
REG_DUR = 0x21
REG_LATENT = 0x22
REG_WINDOW = 0x23
REG_THRESH_ACT = 0x24
REG_THRESH_INACT = 0x25
REG_TIME_INACT = 0x26
REG_ACT_INACT_CTL = 0x27
REG_THRESH_FF = 0x28
REG_TIME_FF = 0x29
REG_TAP_AXES = 0x2A
REG_ACT_TAP_STATUS = 0x2B
REG_BW_RATE = 0x2C
REG_POWER_CTL = 0x2D
REG_INT_ENABLE = 0x2E
REG_INT_MAP = 0x2F
REG_INT_SOURCE = 0x30
REG_DATA_FORMAT = 0x31
REG_DATAX0 = 0x32
REG_DATAX1 = 0x33
REG_DATAY0 = 0x34
REG_DATAY1 = 0x35
REG_DATAZ0 = 0x36
REG_DATAZ1 = 0x37
REG_FIFO_CTL = 0x38
REG_FIFO_STATUS = 0x39

WRITE_MASK = 0x0
READ_MASK = 0x80
MULTIREAD_MASK = 0x40

def get_device_id(self):
    return get_register(REG_DEVICE_ID)

def get_register(address):
  value = spi.xfer2( [ (address & 0x3F) | READ_MASK] )
  return value;

def get_registers(address, count):
  spi.writebytes( [ (address & 0x3F) | READ_MASK | MULTIREAD_MASK ] )
  value = spi.readbytes(count)
  return value

def _convert(self, lsb, msb):
  value = lsb | (msb << 8)
  if value & 0x8000:
    value = -value ^ 0xFFFF
  if not self._full_resolution:
    value = value << self._range
  value *= SCALE_FACTOR
  return value
  
 
def set_register(self, address, value):
  spi.writebytes( [ address, value ] )

def get_axes(self):
  bytes = get_registers(REG_DATAX0, 6)
  x = convert(bytes[0], bytes[1])
  y = convert(bytes[2], bytes[3])
  z = convert(bytes[4], bytes[5])

  return {'x': x,
            'y': y,
            'z': z}

def main():
    # Get device ID
    device_id = get_device_id()
    print("Device ID:", device_id)

    # Get accelerometer data
    axes_data = get_axes()
    print("Accelerometer data:", axes_data)

    # Close SPI connection
    spi.close()

if __name__ == "__main__":
    main()
