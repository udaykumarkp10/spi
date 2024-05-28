import os
from periphery import SPI

# Initialize SPI interface with mode and max_speed
spi = SPI("/dev/spidev2.0", mode=0, max_speed=500000)

# Mount SD card filesystem
os.system("mount /dev/mmcblk0p1 /mnt/sdcard")

# Write data to a file
with open("/mnt/sdcard/test.txt", "w") as f:
    f.write("Hello, SD card!")

# Read data from the file
with open("/mnt/sdcard/test.txt", "r") as f:
    data = f.read()
    print("Data read from file:", data)

# Unmount SD card filesystem
os.system("umount /mnt/sdcard")

# Close SPI interface
spi.close()
