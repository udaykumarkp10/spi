import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from ctypes import cdll, Structure, c_char, c_uint32, c_uint16, c_int, byref
import time

# Load the SOEM shared library
soem = cdll.LoadLibrary("libsoem.so")

# Define constants
EC_TIMEOUTMON = 500

# Define EtherCAT IOmap
IOmap = (c_uint8 * 4096)()

# Define C functions and structures
class ec_slave_info(Structure):
    _fields_ = [("name", c_char * 32),
                ("eep_man", c_uint32),
                ("eep_id", c_uint32),
                ("eep_rev", c_uint32),
                ("state", c_uint16),
                ("ALstatuscode", c_uint16)]

class ec_master_info(Structure):
    _fields_ = [("slaves", c_int),
                ("name", c_char * 32)]

# Initialize SOEM
def ec_init(ifname):
    return soem.ec_init(ifname.encode('utf-8'))

def ec_config_init(uselocaladdr):
    return soem.ec_config_init(uselocaladdr)

def ec_config_map(io_map):
    return soem.ec_config_map(byref(io_map))

def ec_configdc():
    soem.ec_configdc()

def ec_readstate():
    soem.ec_readstate()

def ec_send_processdata():
    soem.ec_send_processdata()

def ec_receive_processdata(timeout):
    return soem.ec_receive_processdata(timeout)

def ec_slavecount():
    return soem.ec_slavecount

def ec_slave(index):
    return ec_slave_info.in_dll(soem, f"ec_slave{index}")

def ec_slave_state(index):
    return soem.ec_slave[index].state

def ec_close():
    soem.ec_close()

# Main function
def main():
    ifname = "eth0"  # Replace with your network interface name

    # Initialize EtherCAT master
    if ec_init(ifname):
        print(f"EtherCAT master initialized on {ifname}")
    else:
        print(f"Failed to initialize EtherCAT master on {ifname}")
        return

    # Initialize configuration
    if ec_config_init(0):
        print(f"{ec_slavecount()} slaves found and configured.")
    else:
        print("No slaves found!")
        ec_close()
        return

    # Map IO
    if ec_config_map(IOmap):
        print("IO map configured.")
    else:
        print("Failed to configure IO map!")
        ec_close()
        return

    # Configure distributed clocks
    ec_configdc()

    print("EtherCAT slaves initialized. Starting operational state...")

    # Set all slaves to operational state
    for i in range(1, ec_slavecount() + 1):
        while ec_slave_state(i) != 8:  # Check if slave is in operational state (0x08)
            ec_send_processdata()
            ec_receive_processdata(EC_TIMEOUTMON)
            ec_readstate()
            time.sleep(0.01)

    print("All slaves are in operational state.")

    # Main loop to send and receive process data
    try:
        while True:
            ec_send_processdata()
            wkc = ec_receive_processdata(EC_TIMEOUTMON)
            if wkc >= 0:
                print(f"Working counter: {wkc}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Process interrupted. Stopping EtherCAT communication...")

    # Close EtherCAT
    ec_close()
    print("EtherCAT master closed.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EtherCAT Communication")

        # Create buttons
        self.button_layout = QVBoxLayout()
        self.buttons = []
        for i in range(1, 6):
            button = QPushButton(f"Send {i}")
            button.clicked.connect(lambda state, x=i: self.send_data(x))
            self.button_layout.addWidget(button)
            self.buttons.append(button)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(self.button_layout)
        self.setCentralWidget(central_widget)

    def send_data(self, data):
        # Here you can trigger the function to send data over EtherCAT
        print(f"Sending data over EtherCAT: {data}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
