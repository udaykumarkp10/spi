import spidev
import time
import ctypes

from ctypes import Union, LittleEndianStructure, c_uint16, c_uint32, c_uint8

# access to EtherCAT registers
RESET_CTL = 0x01F8
ECAT_CSR_DATA = 0x0300
ECAT_CSR_CMD = 0x0304
ECAT_PRAM_RD_ADDR_LEN = 0x0308
ECAT_PRAM_RD_CMD = 0x030C
ECAT_PRAM_WR_ADDR_LEN = 0x0310
ECAT_PRAM_WR_CMD = 0x0314
ECAT_PRAM_RD_DATA = 0x0000
ECAT_PRAM_WR_DATA = 0x0020
ID_REV = 0x0050
IRQ_CFG = 0x0054
INT_STS = 0x0058
INT_EN = 0x005C
BYTE_TEST = 0x0064
HW_CFG = 0x0074
PMT_CTRL = 0x0084
GPT_CFG = 0x008C
GPT_CNT = 0x0090
FREE_RUN = 0x009C


# LAN9252 Datasheet TABLE 12-15: ETHERCAT CORE CSR REGISTERS
TYPE_REG = 0x0000
REV_REG = 0x0001
BUILD_REG_1 = 0x0002
BUILD_REG_2 = 0x0003
FMMU_REG = 0x0004
SYNCMANAGER_REG = 0x0005
RAM_SIZE_REG = 0x0006
PORT_DESCR_REG = 0x0007
ESC_FEATUR_REG_1 = 0x0008
ESC_FEATUR_REG_2 = 0x0009
CONF_STATION_REG_1 = 0x0010
CONF_STATION_REG_2 = 0x0011
CONF_STATION_ALI_REG_1 = 0x0012
CONF_STATION_ALI_REG_2 = 0x0013


# Write Protection Register
WD_REG_EN = 0x0020
WD_REG_PR = 0x0021
ESC_WD_REG_EN = 0x0030
ESC_WD_REG_PR = 0x0031


# Data Link Layer
ESC_RST_REG = 0x0040
ESC_RST_PDI_REG = 0x0041
ECL_DL_CTRL_REG_0 = 0x0100
ECL_DL_CTRL_REG_1 = 0x0101
ECL_DL_CTRL_REG_2 = 0x0102
ECL_DL_CTRL_REG_3 = 0x0103
PHY_R_W_OFF_1 = 0x0108
PHY_R_W_OFF_2 = 0x0109
ECL_DL_STATUS_REG_0 = 0x0110
ECL_DL_STATUS_REG_1 = 0x0111


# Application Layer
AL_CTRL_REG_0 = 0x0120
AL_CTRL_REG_1 = 0x0121
AL_STATUS_REG_0 = 0x0130
AL_STATUS_REG_1 = 0x0131
AL_STATUS_COD_REG_0 = 0x0134
AL_STATUS_COD_REG_1 = 0x0135
RUN_LED_OVERRIDE_REG = 0x0138


# PDI (Process Data Interface)
PDI_CTRL_REG = 0x0140
ESC_CONF_REG = 0x0141
ASIC_CONF_REG_0 = 0x0142
ASIC_CONF_REG_1 = 0x0143
PDI_CONF_REG = 0x0150
SYNC_PDI_CONF_REG = 0x0151
EXT_PDI_CONF_REG_0 = 0x0152
EXT_PDI_CONF_REG_1 = 0x0153


# Interrupts
ECAT_EVENT_MASK_REG_0 = 0x0200
ECAT_EVENT_MASK_REG_1 = 0x0201
AL_EVENT_MASK_REG_0 = 0x0204
AL_EVENT_MASK_REG_1 = 0x0205
AL_EVENT_MASK_REG_2 = 0x0206
AL_EVENT_MASK_REG_3 = 0x0207
ECAT_EVENT_REQ_REG_0 = 0x0210
ECAT_EVENT_REQ_REG_1 = 0x0211
AL_EVENT_REQ_REG_0 = 0x0220
AL_EVENT_REQ_REG_1 = 0x0221
AL_EVENT_REQ_REG_2 = 0x0222
AL_EVENT_REQ_REG_3 = 0x0223


# Error Counters
RX_ERROR_CNT_REG_0 = 0x0300
RX_ERROR_CNT_REG_7 = 0x0307
FWD_RX_ERROR_CNT_REG_0 = 0x0308
FWD_RX_ERROR_CNT_REG_B = 0x030B
ECAT_PRO_UNIT_CNT_ERROR = 0x030C
PDI_CNT_ERROR = 0x030D
PDI_CODE_ERROR = 0x030E
LOST_LINK_CNT_REG_0 = 0x0310
LOST_LINK_CNT_REG_3 = 0x0313

# EEPROM Interface
EEPROM_CONF_REG = 0x0500
EEPROM_PDI_STATE_REG = 0x0501
EEPROM_CTRL_REG_0 = 0x0502
EEPROM_CTRL_REG_1 = 0x0503
EEPROM_ADDR_REG_0 = 0x0504
EEPROM_ADDR_REG_4 = 0x0507
EEPROM_DATA_REG_0 = 0x0508
EEPROM_DATA_REG_4 = 0x050B

# MII Management Interface
MII_MANAGE_CTRL_REG_0 = 0x0510
MII_MANAGE_CTRL_REG_1 = 0x0511
PHY_ADDR_REG = 0x0512
PHY_REGISTER_ADDR_REG = 0x0513
PHY_DATA_REG_0 = 0x0514
PHY_DATA_REG_1 = 0x0515
MII_MANAGE_ECAT_REG = 0x0516
MII_MANAGE_PDI_REG = 0x0517
AL_STATUS = 0x0130
WDOG_STATUS = 0x0440

# LAN9252 flags
ECAT_CSR_BUSY = 0x80
PRAM_READ_BUSY = 0x80
PRAM_READ_AVAIL = 0x01
PRAM_WRITE_AVAIL = 0x01
READY = 0x08000000
DIGITAL_RST = 0x00000001
ETHERCAT_RST = 0x00000040

# EtherCAT flags
ESM_INIT = 0x01                  # init
ESM_PREOP = 0x02                  # pre-operational
ESM_BOOT = 0x03                  # bootstrap
ESM_SAFEOP = 0x04                  # safe-operational
ESM_OP = 0x08                  # operational

# ESC commands
ESC_WRITE = 0x80
ESC_READ = 0xC0

# SPI
COMM_SPI_READ = 0x03
COMM_SPI_WRITE = 0x02
DUMMY_BYTE = 0xFF


# etc scan variables
WatchDog = False
Operational = False


chip_id = ctypes.c_uint32(0)

# Define input variables as unsigned 32-bit integers
etc_in_0 = ctypes.c_uint32(0)
etc_in_1 = ctypes.c_uint32(0)
etc_in_2 = ctypes.c_uint32(0)
etc_in_3 = ctypes.c_uint32(0)
etc_in_4 = ctypes.c_uint32(0)
etc_in_5 = ctypes.c_uint32(0)
etc_in_6 = ctypes.c_uint32(0)
etc_in_7 = ctypes.c_uint32(0)

# Define output variables as unsigned 32-bit integers
etc_out_0 = ctypes.c_uint32(0)
etc_out_1 = ctypes.c_uint32(0)
etc_out_2 = ctypes.c_uint32(0)
etc_out_3 = ctypes.c_uint32(0)
etc_out_4 = ctypes.c_uint32(0)
etc_out_5 = ctypes.c_uint32(0)
etc_out_6 = ctypes.c_uint32(0)
etc_out_7 = ctypes.c_uint32(0)


class UWORD(Union):
    _fields_ = [("LANWord", c_uint16),                 # uint16_t LANWord
                ("LANByte", c_uint8 * 2)]              # uint8_t LANByte[2]

class ULONG(Union):
    _fields_ = [("LANLong", c_uint32),                # uint32_t LANLong
                ("LANWord", c_uint16 * 2),             # uint16_t LANWord[2]
                ("LANByte", c_uint8 * 4)]             # uint8_t LANByte[4]

class PROCBUFFER(ctypes.Union):
    _fields_ = [("LANByte", ctypes.c_uint8 * 32),    # uint8_t LANByte[32]
                ("LANLong", ctypes.c_uint32 * 8)]    # uint32_t LANLong[8]
                # ("LANFloat", ctypes.c_float * 8)]    # float LANFloat[8]



# Define external buffer instances
Etc_Buffer_Out = PROCBUFFER()
Etc_Buffer_In = PROCBUFFER()

# Zero initialize the LANByte array
for i in range(32):
    Etc_Buffer_Out.LANByte[i] = 0
    Etc_Buffer_In.LANByte[i] = 0

# Open SPI device

spi = spidev.SpiDev()
spi.open(2, 0)  # Open SPI bus 2, device 0
spi.max_speed_hz = 3000000   # 3MHz
spi.bits_per_word = 8  # Data size is 8 bits (SPI_DATASIZE_8BIT)
spi.lsbfirst = False  # MSB first (SPI_FIRSTBIT_MSB)
spi.threewire = False  # Use 3-wire mode (SPI_DIRECTION_2LINES)
spi.cshigh = False  # Chip Select active low

# Etc_Buffer_Out.LANByte[:] = [0] * 32     #  etc routines
# Etc_Buffer_In.LANByte[:] = [0] * 32      # etc routines

def Etc_Read_Reg(address, length):
    Result = ULONG()  # Initialize Result as ULONG instance
    Addr = UWORD()    # Initialize Addr as UWORD instance and set address
    xfrbuf = (ctypes.c_uint8 * 7)()  # Create buffer for SPI xfer2

    Addr.LANWord = address

    xfrbuf[0] = COMM_SPI_READ  # SPI read command
    xfrbuf[1] = Addr.LANByte[1]  # Address high byte
    xfrbuf[2] = Addr.LANByte[0]  # Address low byte

    for i in range(length):
        xfrbuf[i + 3] = DUMMY_BYTE  # Fill dummy bytes after address bytes

    # Convert ctypes array to list of bytes
    xfrbuf_list = [byte for byte in xfrbuf]

    response = spi.xfer2(xfrbuf_list)

    # response = spi.xfer2(list(xfrbuf))  # Perform SPI xfer2 and receive response
    Result.LANLong = 0

    for i in range(length):
        Result.LANByte[i] = response[i + 3]  # Assign received bytes to Result.LANByte[i]
    return Result.LANLong


def Etc_Write_Reg(address, DataOut):
    Data = ULONG()
    Addr = UWORD()
    xfrbuf = (ctypes.c_uint8 * 7)()  # Create buffer for SPI xfer2

    Addr.LANWord = address
    Data.LANLong = DataOut

    xfrbuf[0] = COMM_SPI_WRITE     # SPI write command
    xfrbuf[1] = Addr.LANByte[1]    # address of the register
    xfrbuf[2] = Addr.LANByte[0]    # to read, MsByte first
    
    for i in range(4):
        xfrbuf[i+3] = Data.LANByte[i]       # Fill data bytes, lsb

    xfrbuf_list = [byte for byte in xfrbuf]

    response = spi.xfer2(xfrbuf_list)


# read an indirectly addressable register

def Etc_Read_Reg_Wait(address, length):
    TempLong = ULONG()
    Addr = UWORD()

    Addr.LANWord = address
    TempLong.LANByte[0] = Addr.LANByte[0]     #address of the register
    TempLong.LANByte[1] = Addr.LANByte[1]     #to read, LsByte first
    TempLong.LANByte[2] = length                   #number of bytes to read
    TempLong.LANByte[3] = ESC_READ                   # ESC read

    Etc_Write_Reg(ECAT_CSR_CMD, TempLong.LANLong) # write the command
    TempLong.LANByte[3] = ECAT_CSR_BUSY

    TempLong.LANLong = Etc_Read_Reg(ECAT_CSR_CMD, 4)
    while (TempLong.LANByte[3] & ECAT_CSR_BUSY):   # wait for command execution
        TempLong.LANLong = Etc_Read_Reg(ECAT_CSR_CMD, 4)

    TempLong.LANLong = Etc_Read_Reg(ECAT_CSR_DATA, length)     # read the requested register

    return TempLong.LANLong

# read from process ram fifo
def Etc_Read_Fifo():
    TempLong = ULONG()
    xfrbuf = (ctypes.c_uint8 * 35)()  # Create buffer for SPI xfer2

    Etc_Write_Reg(ECAT_PRAM_RD_ADDR_LEN, 0x00201000)     # we always read 32 bytes (0x0020), output process ram offset 0x1000
    Etc_Write_Reg(ECAT_PRAM_RD_CMD, 0x80000000)         # start command
    TempLong.LANLong = 0

    TempLong.LANLong = Etc_Read_Reg(ECAT_PRAM_RD_CMD, 4)

    while (not (TempLong.LANByte[0] & PRAM_READ_AVAIL) or (TempLong.LANByte[1] != 8)):  # Corrected logical OR operator
        TempLong.LANLong = Etc_Read_Reg(ECAT_PRAM_RD_CMD, 4)

    xfrbuf[0] = COMM_SPI_READ                       # SPI read command
    xfrbuf[1] = 0x00                               # address of the read
    xfrbuf[2] = 0x00                               # fifo MsByte first

    for i in range(32):
        xfrbuf[i+3] = DUMMY_BYTE

    xfrbuf_list = [byte for byte in xfrbuf]

    # Transmit function
    response = spi.xfer2(xfrbuf_list)

    for i in range(32):        # 32 bytes read data to usable buffer
        Etc_Buffer_Out.LANByte[i] = xfrbuf_list[i+3]          # Need to check


# write to the process ram fifo

def Etc_Write_Fifo():
    TempLong = ULONG()
    xfrbuf = (ctypes.c_uint8 * 35)()    # buffer for spi xfr

    Etc_Write_Reg(ECAT_PRAM_WR_ADDR_LEN, 0x00201200)     # we always write 32 bytes (0x0020), input process ram offset 0x1200
    Etc_Write_Reg(ECAT_PRAM_WR_CMD, 0x80000000)         # start command
    TempLong.LANLong = 0

    TempLong.LANLong = Etc_Read_Reg(ECAT_PRAM_WR_CMD, 4)

    while (not (TempLong.LANByte[0] & PRAM_WRITE_AVAIL) or (TempLong.LANByte[1] < 8)):
	    TempLong.LANLong = Etc_Read_Reg(ECAT_PRAM_WR_CMD, 4)
	      
    xfrbuf[0] = COMM_SPI_WRITE              # SPI write command
    xfrbuf[1] = 0x00                        # address of the write fifo
    xfrbuf[2] = 0x20                        # MsByte first

    for i in range(32):                      # 32 bytes write loop
        xfrbuf[i+3] = Etc_Buffer_In.LANByte[i]

    xfrbuf_list = [byte for byte in xfrbuf]

    # Transmit function
    response = spi.xfer2(xfrbuf_list)


# initialize / check the etc interface on SPI, return true if initialization is ok
def etc_init():
    TempLong = ULONG()

    Etc_Write_Reg(RESET_CTL, (DIGITAL_RST & ETHERCAT_RST))  # Need to check "AND" Operator
    time.sleep(0.1)
    TempLong.LANLong = Etc_Read_Reg(BYTE_TEST, 4)  # read test register

    # Print the value of TempLong
    # print("Value of TempLong:", TempLong.LANLong)

    if TempLong.LANLong != 0x87654321:
        print("Bad response received from Etc Test command, data received =", TempLong.LANLong)
        return False

    TempLong.LANLong = Etc_Read_Reg(HW_CFG, 4)  # check also the READY flag

    if (TempLong.LANLong & READY) == 0:
        print("Ready not received from Etc HW Cfg, data received =", TempLong.LANLong)
        return False

    print("Etc Test Command succeeded\n")

    print("EtherCAT Chip ID = ", end="")
    chip_id = Etc_Read_Reg(ID_REV, 4)  # Assuming Etc_Read_Reg is a function that returns the chip ID
    print(chip_id)

    return True
  

# one scan of etc

def etc_scan():
    global WatchDog, Operational
    WatchDog = False
    Operational = False
    TempLong = ULONG()
    Status = 0

    TempLong.LANLong = Etc_Read_Reg_Wait(WDOG_STATUS, 1) # read watchdog status

    if ((TempLong.LANByte[0] & 0x01) == 0x01):
        WatchDog = False
    else:
        WatchDog = True
        # print("Etc Watchdog active\n")

    TempLong.LANLong = Etc_Read_Reg_Wait(AL_STATUS_REG_0, 1)   # read the EtherCAT State Machine status
    Status = TempLong.LANByte[0] & 0x0F        # Need to check this "and"

    if Status == ESM_OP:
        Operational = True    # to see if we are in operational state
    else:
        Operational = False     # set/reset the corresponding flag
        # print("Etc not operational\n")


    # process data xfer2t
    if WatchDog or not Operational:
        for i in range(8):
            Etc_Buffer_Out.LANLong[i] = 0
    else:
        # print("Read fifo\n")
        Etc_Read_Fifo()

    Etc_Write_Fifo()

    if WatchDog:
        Status |= 0x80

    return Status


def main():
    # Initialize EtherCAT interface
    etc_init()
    # Read EtherCAT chip ID
    chip_id = Etc_Read_Reg(ID_REV, 4)  # Using a dummy ID_REV address
    print("EtherCAT Chip ID:", chip_id)
    
    while True:
        # Simulate scanning for EtherCAT data (replace with actual scan function)
        etc_scan()
        
        # Read data from Etc_Buffer_Out (data sent from TwinCAT)
        etc_out_0 = Etc_Buffer_Out.LANLong[0]
        etc_out_1 = Etc_Buffer_Out.LANLong[1]   
        etc_out_2 = Etc_Buffer_Out.LANLong[2]  
        etc_out_3 = Etc_Buffer_Out.LANLong[3]
        etc_out_4 = Etc_Buffer_Out.LANLong[4]
        etc_out_5 = Etc_Buffer_Out.LANLong[5]
        etc_out_6 = Etc_Buffer_Out.LANLong[6]
        etc_out_7 = Etc_Buffer_Out.LANLong[7]
        
        # Print received data from TwinCAT
        print(f"Received from TwinCAT: {etc_out_0}, {etc_out_1}, {etc_out_2}, {etc_out_3}, {etc_out_4}, {etc_out_5}, {etc_out_6}, {etc_out_7}")
        
        # Write data to Etc_Buffer_In (data sent to TwinCAT)
        Etc_Buffer_In.LANLong[0] = 1
        Etc_Buffer_In.LANLong[1] = 2
        
        # Wait for 0.1 seconds before next iteration
        time.sleep(0.1)

if __name__ == "__main__":
    main()  # Call the main function
