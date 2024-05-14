import sys

if sys.byteorder == 'little':
    print("Your system is using little-endian byte order.")
elif sys.byteorder == 'big':
    print("Your system is using big-endian byte order.")
else:
    print("Unable to determine byte order.")
