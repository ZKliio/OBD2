import serial

ser = serial.Serial('COM4', 115200, timeout=1)

# Send CAN frame (based on the protocol from Waveshare)
frame = b'\xAA\x55...'  # You'll need to refer to Waveshare’s serial command format
ser.write(frame)

response = ser.read(100)
print(response)
