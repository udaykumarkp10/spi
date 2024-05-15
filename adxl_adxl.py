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

# Full Resolution scale factor (0x100 LSB/g ~= 3.9/1000 mg/LSB)
SCALE_FACTOR = 1/0x100

WRITE_MASK = 0x0
READ_MASK = 0x80
MULTIREAD_MASK = 0x40
full_resolution = True

# SPI setup
spi = spidev.SpiDev()
spi.open(2, 0)  # Assuming SPI bus 0, device 0
spi.max_speed_hz = 5000000
spi.mode = 0b11

# Additional settings
spi.bits_per_word = 8  # Data size is 8 bits (SPI_DATASIZE_8BIT)
spi.cshigh = False  # Use hardware CS
spi.lsbfirst = False  # MSB first (SPI_FIRSTBIT_MSB)
spi.threewire = False  # Use 3-wire mode (SPI_DIRECTION_2LINES)

def get_device_id():
    return get_register(REG_DEVICE_ID)

def set_range(range, full_resolution=True):
    """ Set the G range and the resolution. Valid range values are 2, 4, 8, 16. Full resolution set either 10-bit or 13-bit resolution """
    if range == 2:
      range_code = 0x0
    elif range == 4:
      range_code = 0x1
    elif range == 8:
      range_code = 0x2
    elif range == 16:
      range_code = 0x3
    else:
      raise ValueError("invalid range [" + str(range) + "] expected one of [2, 4, 8, 16]")

    range = range_code
    full_resolution = full_resolution
    send_data_format()


def set_data_rate(hz, low_power=False):
    if hz >= 3200:
      rate = 3200
      rate_code = 0b1111
    elif hz >= 1600 and hz < 3200:
      rate = 1600
      rate_code = 0b1110
    elif hz >= 800 and hz < 1600:
      rate = 800
      rate_code = 0b1101
    elif hz >= 400 and hz < 800:
      rate = 400
      rate_code = 0b1100
    elif hz >= 200 and hz < 400:
      rate = 200
      rate_code = 0b1011
    elif hz >= 100 and hz < 200:
      rate = 100
      rate_code = 0b1010
    elif hz >= 50 and hz < 100:
      rate = 50
      rate_code = 0b1001
    elif hz >= 25 and hz < 50:
      rate = 25
      rate_code = 0b1000
    elif hz >= 25/2 and hz < 25:
      rate = 25/2
      rate_code = 0b0111
    elif hz >= 25/4 and hz < 25/2:
      rate = 25/4
      rate_code = 0b0110
    elif hz >= 25/8 and hz < 25/4:
      rate = 25/8
      rate_code = 0b0101
    elif hz >= 25/16 and hz < 25/8:
      rate = 25/16
      rate_code = 0b0100
    elif hz >= 25/32 and hz < 25/16:
      rate = 25/32
      rate_code = 0b0011
    elif hz >= 25/64 and hz < 25/32:
      rate = 25/64
      rate_code = 0b0010
    elif hz >= 25/128 and hz < 25/64:
      rate = 25/128
      rate_code = 0b0001
    elif hz < 25/128:
      rate = 25/256
      rate_code = 0
    
    if low_power:
      rate_code = rate_code | 0x10

def get_register(address):
  value = spi.xfer2( [ (address & 0x3F) | READ_MASK] )
  return value;

def get_registers(address, count):
  spi.writebytes( [ (address & 0x3F) | READ_MASK | MULTIREAD_MASK ] )
  value = spi.readbytes(count)
  return value

def convert(lsb, msb):
  value = lsb | (msb << 8)
  if value & 0x8000:
    value = -value ^ 0xFFFF
  if not full_resolution:
    value = value << self._range
  value *= SCALE_FACTOR
  return value
  
 
def set_register(address, value):
  spi.writebytes( [ address, value ] )

def get_axes():
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

    set_range(16)
    set_data_rate(100)

    while(True):
        axes_data = get_axes()
        print("Accelerometer data:", axes_data)
        time.sleep(0.2)

    # Close SPI connection
    spi.close()

if __name__ == "__main__":
    main()
