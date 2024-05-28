import os
from periphery import SPI

# Initialize SPI interface with mode and max_speed
spi = SPI("/dev/spidev2.0", mode=0, max_speed=500000)

# Create mount point if it doesn't exist
mount_point = "/mnt/sdcard"
if not os.path.exists(mount_point):
    os.makedirs(mount_point)

# Mount SD card filesystem
os.system("mount /dev/mmcblk0p1 " + mount_point)

# Write data to a file
with open(os.path.join(mount_point, "test.txt"), "w") as f:
    f.write("Hello, SD card!")

# Read data from the file
with open(os.path.join(mount_point, "test.txt"), "r") as f:
    data = f.read()
    print("Data read from file:", data)

# Unmount SD card filesystem
os.system("umount " + mount_point)

# Close SPI interface
spi.close()
