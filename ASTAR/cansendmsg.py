import can
import time

# Setup CAN bus
bus = can.interface.Bus(channel='can0', bustype='socketcan')  # Adjust to your platform

# UDS request: Read Data by Identifier (0x22 F1 90)
msg = can.Message(arbitration_id=0x7E0,  # Request to ECU
                  data=[0x03, 0x22, 0xF1, 0x90, 0x00, 0x00, 0x00, 0x00],
                  is_extended_id=False)

print("Sending UDS request: 0x22 F1 90")
bus.send(msg)

# Wait for response
start = time.time()
timeout = 2  # seconds

while True:
    response = bus.recv(1.0)
    if response is None:
        if time.time() - start > timeout:
            print("No response within timeout.")
            break
    elif response.arbitration_id == 0x7E8:
        print(f"Received response: {response.data.hex()}")
        break
