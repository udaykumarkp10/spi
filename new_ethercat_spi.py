import spidev
import time

# Constants for LAN9252
ID_REV = 0x0000
WDOG_STATUS = 0x0440
AL_STATUS_REG_0 = 0x0130
ESM_OP = 0x08

class LAN9252:
    def __init__(self, bus=2, device=0, max_speed_hz=50000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = 0b11

    def read_register(self, address, size=4):
        tx = [0x03, (address >> 8) & 0xFF, address & 0xFF] + [0x00] * size
        rx = self.spi.xfer2(tx)
        return rx[3:]

    def write_register(self, address, data):
        tx = [0x02, (address >> 8) & 0xFF, address & 0xFF] + data
        self.spi.xfer2(tx)

    def init_device(self):
        id_rev = self.read_register(ID_REV)
        print(f"ID_REV: {id_rev}")

    def close(self):
        self.spi.close()

def etc_init():
    lan9252 = LAN9252()
    lan9252.init_device()
    return lan9252

def etc_scan(lan9252):
    # Read watchdog status
    watchdog_status = lan9252.read_register(WDOG_STATUS, 1)
    watchdog_active = (watchdog_status[0] & 0x01) == 0
    print("Watchdog active" if watchdog_active else "Watchdog not active")

    # Read EtherCAT state machine status
    al_status = lan9252.read_register(AL_STATUS_REG_0, 1)
    operational = (al_status[0] & 0x0F) == ESM_OP
    print("Operational" if operational else "Not operational")

    # Example: reset buffer if watchdog is active or not operational
    if watchdog_active or not operational:
        buffer_out = [0] * 8
        lan9252.write_register(0x0000, buffer_out)  # Example buffer address
    else:
        print("Reading FIFO (Not implemented)")

    print("Writing FIFO (Not implemented)")
    # You would implement Etc_Read_Fifo and Etc_Write_Fifo similarly

def main():
    lan9252 = etc_init()
    if lan9252:
        etc_scan(lan9252)
        lan9252.close()
    else:
        print("EtherCAT initialization failed")

if __name__ == "__main__":
    main()
