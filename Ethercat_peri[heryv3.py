from periphery import SPI
import time
import ctypes
import gpiod

from gpiod.line import Direction, Value

from ctypes import Union, LittleEndianStructure, c_uint16, c_uint32, c_uint8

# Define GPIO parameters
LINE = 2  # Change this to the GPIO line you want to control

# Define EtherCAT registers
BYTE_TEST = 0x0064

# SPI constants
COMM_SPI_READ = 0x03
DUMMY_BYTE = 0xFF

# Open SPI device
spi = SPI("/dev/spidev2.0", 3, 3000000)  # SPI bus 2, device 0, 3 MHz
spi.bits_per_word = 8  # Data size is 8 bits
spi.lsbfirst = False   # MSB first
spi.threewire = False  # Use 4-wire mode
spi.cshigh = False     # Chip Select active low

class ULONG(Union):
    _fields_ = [("LANLong", c_uint32),    # uint32_t LANLong
                ("LANByte", c_uint8 * 4)] # uint8_t LANByte[4]


"""
 
def Etc_Read_Reg(request, address, length):
    Result = ULONG()  # Initialize Result as ULONG instance
    Addr = c_uint16(address)  # Initialize Addr as c_uint16 and set address

    xfrbuf = (ctypes.c_uint8 * 7)()  # Create buffer for SPI transfer

    xfrbuf[0] = COMM_SPI_READ  # SPI read command
    xfrbuf[1] = Addr.value >> 8  # Address high byte
    xfrbuf[2] = Addr.value & 0xFF  # Address low byte

    for i in range(length):
        xfrbuf[i + 3] = DUMMY_BYTE  # Fill dummy bytes after address bytes

    # Convert ctypes array to list of bytes
    xfrbuf_list = [byte for byte in xfrbuf]

    request.set_value(LINE, Value.INACTIVE)
    response = spi.transfer(xfrbuf_list)
    request.set_value(LINE, Value.ACTIVE)

    # Convert list of bytes to ctypes array
    response_array = (ctypes.c_uint8 * len(response))(*response)

    # Assign received bytes to Result
    Result.LANLong = 0
    for i in range(length):
        Result.LANByte[i] = response_array[i + 3]

    print(Result.LANLong)
    return Result.LANLong

"""


def Etc_Read_Reg(address, length):
    Result = ULONG()  # Initialize Result as ULONG instance
    Addr = UWORD()    # Initialize Addr as UWORD instance and set address
    xfrbuf = (ctypes.c_uint8 * 7)()  # Create buffer for SPI transfer

    Addr.LANWord = address

    xfrbuf[0] = COMM_SPI_READ  # SPI read command
    xfrbuf[1] = Addr.LANByte[1]  # Address high byte
    xfrbuf[2] = Addr.LANByte[0]  # Address low byte

    print()
    print("Entered Read_reg")
    print()
    print("xfrbuf before filling: ", end="")
    for i in range(3):
        print("{:02X} ".format(xfrbuf[i]), end="")          

    for i in range(length):
        xfrbuf[i + 3] = DUMMY_BYTE  # Fill dummy bytes after address bytes

    print("\nxfrbuf after filling: ", end="")
    for i in range(7):
        print("{:02X} ".format(xfrbuf[i]), end="")

    request.set_value(LINE, Value.INACTIVE)
    response = spi.transfer(xfrbuf_list)
    request.set_value(LINE, Value.ACTIVE)


    # print("\nresponse:", response)  # Print the response received from spi.xfer(xfrbuf)

    print()
    print("Response in hexadecimal:")
    for byte in response:
        print("{:02X}".format(byte), end=" ")

    # response = spi.xfer2(list(xfrbuf))  # Perform SPI transfer and receive response
    Result.LANLong = 0

    for i in range(length):
        Result.LANByte[i] = response[i + 3]  # Assign received bytes to Result.LANByte[i]
    return Result.LANLong


def etc_init():
    # Initialize EtherCAT interface
    with gpiod.request_lines(
        "/dev/gpiochip0",
        consumer="Ethercat_peripheryv2",
        config={
	        LINE: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=Value.ACTIVE
            )
        },
    ) as request:
        # Check if SPI communication works
        TempLong = Etc_Read_Reg(request, BYTE_TEST, 4)






if __name__ == "__main__":
    while True:
        if not etc_init():
            print("EtherCAT initialization failed")
	    
        time.sleep(0.2)  # Sleep for 0.2 seconds before running again


