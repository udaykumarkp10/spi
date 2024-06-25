import spidev

# Constants for LAN9252
ID_REV = 0x0000

class LAN9252:
    def __init__(self, bus=0, device=0, max_speed_hz=50000):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = 0b11

    def read_register(self, address, size=4):
        tx = [0x03, (address >> 8) & 0xFF, address & 0xFF] + [0x00] * size
        rx = self.spi.xfer2(tx)
        return rx[3:]

    def close(self):
        self.spi.close()

def check_chip_id():
    lan9252 = LAN9252()
    id_rev = lan9252.read_register(ID_REV)
    lan9252.close()
    id_rev_value = int.from_bytes(id_rev, byteorder='big')
    print(f"ID_REV: {id_rev_value:#010x}")

if __name__ == "__main__":
    check_chip_id()
