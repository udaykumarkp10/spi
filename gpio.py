from periphery import GPIO
import time

# GPIO number corresponding to gpio4.IO[11] (SODIMM Pin 86)
gpio_number = 107

# Open the GPIO pin
cs_pin = GPIO(gpio_number, "out")

# Function to set CS pin low (active)
def activate_cs():
    cs_pin.write(False)
    print("CS pin set to LOW (active)")

# Function to set CS pin high (inactive)
def deactivate_cs():
    cs_pin.write(True)
    print("CS pin set to HIGH (inactive)")

# Initialize CS pin to high (inactive)
deactivate_cs()

# Example usage
try:
    # Activate CS pin
    activate_cs()
    
    # Turn on LED
    print("LED should be ON")
    time.sleep(1)  # Simulate SPI operation duration
    
    # Deactivate CS pin
    deactivate_cs()
    
    # Turn off LED
    print("LED should be OFF")
    time.sleep(1)

finally:
    # Clean up and close the GPIO pin
    cs_pin.close()
