import can
import time

def setup_bus(channel_num, bitrate=500000, data_bitrate=2000000):
    bus = can.interface.Bus(
        interface='zlgcan',
        device_type='USBCANFD',  # required for Waveshare USB-CAN-FD-B
        channel=str(channel_num),
        bitrate=bitrate,
        data_bitrate=data_bitrate,
        fd=True,
        configs={
            "acc_code": 0,
            "acc_mask": 0xFFFFFFFF,
            "filter": 0,
            "mode": 0,
        }
    )

    print(f"[INFO] CAN{channel_num+1} Initialized.")
    return bus

def send_message(bus, channel_name, msg_id, data):
    msg = can.Message(
        arbitration_id=msg_id,
        data=data,
        is_fd=True
    )
    try:
        bus.send(msg)
        print(f"[{channel_name}] Sent ID: {hex(msg.arbitration_id)} Data: {msg.data.hex()}")
    except can.CanError as e:
        print(f"[ERROR] Send failed on {channel_name}: {e}")

if __name__ == "__main__":
    bus1 = setup_bus(channel_num=0)  # CAN1
    bus2 = setup_bus(channel_num=1)  # CAN2

    data1 = [0x01, 0x02, 0x03, 0x04]
    data2 = [0xA1, 0xB2, 0xC3, 0xD4]

    while True:
        send_message(bus1, "CAN1", 0x100, data1)
        send_message(bus2, "CAN2", 0x200, data2)
        time.sleep(1)  # Delay between sends

#!/usr/bin/env python

# """
# This example shows how sending a single message works.
# """

# import can


# def send_one():
#     """Sends a single message."""

#     # this uses the default configuration (for example from the config file)
#     # see https://python-can.readthedocs.io/en/stable/configuration.html
#     with can.Bus() as bus:
#         # Using specific buses works similar:
#         # bus = can.Bus(interface='socketcan', channel='vcan0', bitrate=250000)
#         # bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=250000)
#         # bus = can.Bus(interface='ixxat', channel=0, bitrate=250000)
#         bus = can.Bus(interface='vector', app_name='CANalyzer', channel=0, bitrate=250000)
#         # ...

#         msg = can.Message(
#             arbitration_id=0xC0FFEE, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True
#         )

#         try:
#             bus.send(msg)
#             print(f"Message sent on {bus.channel_info}")
#         except can.CanError:
#             print("Message NOT sent")


# if __name__ == "__main__":
#     send_one()