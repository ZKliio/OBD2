#
#python3.8.8 64位（python 32位要用32位的DLL）
#
# V2.0  -- add CAN frame send and recv. add close dev. add filter.
#
from ctypes import *
import time


VCI_USBCAN2 = 41
STATUS_OK = 1
INVALID_DEVICE_HANDLE  = 0
INVALID_CHANNEL_HANDLE = 0
TYPE_CAN = 0
TYPE_CANFD = 1

class VCI_INIT_CONFIG(Structure):  
    _fields_ = [("AccCode", c_uint),
                ("AccMask", c_uint),
                ("Reserved", c_uint),
                ("Filter", c_ubyte),
                ("Timing0", c_ubyte),
                ("Timing1", c_ubyte),
                ("Mode", c_ubyte)
                ]  
class VCI_CAN_OBJ(Structure):  
    _fields_ = [("ID", c_uint),
                ("TimeStamp", c_uint),
                ("TimeFlag", c_ubyte),
                ("SendType", c_ubyte),
                ("RemoteFlag", c_ubyte),
                ("ExternFlag", c_ubyte),
                ("DataLen", c_ubyte),
                ("Data", c_ubyte*8),
                ("Reserved", c_ubyte*3)
                ] 
 
### structure
class _ZCAN_CHANNEL_CAN_INIT_CONFIG(Structure):
    _fields_ = [("acc_code", c_uint),
                ("acc_mask", c_uint),
                ("reserved", c_uint),
                ("filter",   c_ubyte),
                ("timing0",  c_ubyte),
                ("timing1",  c_ubyte),
                ("mode",     c_ubyte)]

class _ZCAN_CHANNEL_CANFD_INIT_CONFIG(Structure):
    _fields_ = [("acc_code",     c_uint),
                ("acc_mask",     c_uint),
                ("abit_timing",  c_uint),
                ("dbit_timing",  c_uint),
                ("brp",          c_uint),
                ("filter",       c_ubyte),
                ("mode",         c_ubyte),
                ("pad",          c_ushort),
                ("reserved",     c_uint)]

class _ZCAN_CHANNEL_INIT_CONFIG(Union):
    _fields_ = [("can", _ZCAN_CHANNEL_CAN_INIT_CONFIG), ("canfd", _ZCAN_CHANNEL_CANFD_INIT_CONFIG)]

class ZCAN_CHANNEL_INIT_CONFIG(Structure):
    _fields_ = [("can_type", c_uint),
                ("config", _ZCAN_CHANNEL_INIT_CONFIG)]
				
class ZCAN_CAN_FRAME(Structure):
    _fields_ = [("can_id",  c_uint, 29),
                ("err",     c_uint, 1),
                ("rtr",     c_uint, 1),
                ("eff",     c_uint, 1), 
                ("can_dlc", c_ubyte),
                ("__pad",   c_ubyte),
                ("__res0",  c_ubyte),
                ("__res1",  c_ubyte),
                ("data",    c_ubyte * 8)]

class ZCAN_CANFD_FRAME(Structure):
    _fields_ = [("can_id", c_uint, 29), 
                ("err",    c_uint, 1),
                ("rtr",    c_uint, 1),
                ("eff",    c_uint, 1), 
                ("len",    c_ubyte),
                ("brs",    c_ubyte, 1),
                ("esi",    c_ubyte, 1),
                ("__res",  c_ubyte, 6),
                ("__res0", c_ubyte),
                ("__res1", c_ubyte),
                ("data",   c_ubyte * 64)]

				
class ZCAN_Transmit_Data(Structure):
    _fields_ = [("frame", ZCAN_CAN_FRAME), ("transmit_type", c_uint)]

class ZCAN_Receive_Data(Structure):
    _fields_  = [("frame", ZCAN_CAN_FRAME), ("timestamp", c_ulonglong)]

class ZCAN_TransmitFD_Data(Structure):
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("transmit_type", c_uint)]

class ZCAN_ReceiveFD_Data(Structure):
    _fields_ = [("frame", ZCAN_CANFD_FRAME), ("timestamp", c_ulonglong)]

	
CanDLLName = './ControlCANFD.dll' #把DLL放到对应的目录下
# canDLL = windll.LoadLibrary('./libcontrolcanfd.so') # used for windows only platform
#Linux系统下使用下面语句，编译命令：python3 cxcanfd.py
canDLL = cdll.LoadLibrary('./ControlCANFD.dll') # cdll works for all the platform 

print('########################################################')
print('## Chuang Xin USBCANFD python(x64) test program V2.0 ###')
print('########################################################')
print(CanDLLName)


canDLL.ZCAN_OpenDevice.restype = c_void_p
canDLL.ZCAN_SetAbitBaud.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_SetDbitBaud.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_SetCANFDStandard.argtypes = (c_void_p, c_ulong, c_ulong)
canDLL.ZCAN_InitCAN.argtypes = (c_void_p, c_ulong, c_void_p)
canDLL.ZCAN_InitCAN.restype = c_void_p
canDLL.ZCAN_StartCAN.argtypes = (c_void_p,)
canDLL.ZCAN_Transmit.argtypes = (c_void_p, c_void_p, c_ulong)
canDLL.ZCAN_TransmitFD.argtypes = (c_void_p, c_void_p, c_ulong)
canDLL.ZCAN_GetReceiveNum.argtypes = (c_void_p, c_ulong)
canDLL.ZCAN_Receive.argtypes = (c_void_p, c_void_p, c_ulong, c_long)
canDLL.ZCAN_ReceiveFD.argtypes = (c_void_p, c_void_p, c_ulong, c_long)
canDLL.ZCAN_ResetCAN.argtypes = (c_void_p,)
canDLL.ZCAN_CloseDevice.argtypes = (c_void_p,)

canDLL.ZCAN_ClearFilter.argtypes=(c_void_p,)
canDLL.ZCAN_AckFilter.argtypes=(c_void_p,)
canDLL.ZCAN_SetFilterMode.argtypes=(c_void_p,c_ulong)
canDLL.ZCAN_SetFilterStartID.argtypes=(c_void_p,c_ulong)
canDLL.ZCAN_SetFilterEndID.argtypes=(c_void_p,c_ulong)

#打开设备 
#Device 0
m_dev = canDLL.ZCAN_OpenDevice(VCI_USBCAN2, 0, 0)
if m_dev == INVALID_DEVICE_HANDLE:
    print("Open Device failed!")
    exit(0)
#print("Open Device OK, device handle:0x%x." %(m_dev))
print(f"Open Device OK, device handle: 0x{m_dev:x}") 

#设置通道0 仲裁域波特率：1M, 数据域波特率：5M
# ret = canDLL.ZCAN_SetAbitBaud(m_dev,0,1000000) #CANFD buad rate
ret = canDLL.ZCAN_SetAbitBaud(m_dev,0,500000) #CAN buad rate
if ret != STATUS_OK:
	print("Set CAN0 abit:500k failed!")
	exit(0)
print("Set CAN0 abit:500k OK!");
ret = canDLL.ZCAN_SetDbitBaud(m_dev,0,500000)
if ret != STATUS_OK:
	print("Set CAN0 dbit:500k failed!")
	exit(0)
print("Set CAN0 dbit:500k OK!");

#设置通道1 仲裁域波特率：1M, 数据域波特率：5M
# Setting buad rate: Abit 1Mbps, Dbit 5Mbps
# ret = canDLL.ZCAN_SetAbitBaud(m_dev,1,1000000) #CANFD buad rate
ret = canDLL.ZCAN_SetAbitBaud(m_dev,1,500000) #CAN buad rate
if ret != STATUS_OK:
	print("Set CAN1 abit:5k failed!")
	exit(0)
print("Set CAN1 abit:5k OK!");
ret = canDLL.ZCAN_SetDbitBaud(m_dev,1,500000)
if ret != STATUS_OK:
	print("Set CAN1 dbit:5k failed!")
	exit(0)
print("Set CAN1 dbit:5k OK!");

#设置通道0,1 FDMode : ISO
# NOT using as we're using CAN
ret = canDLL.ZCAN_SetCANFDStandard(m_dev,0,0)
if ret != STATUS_OK:
	print("Set CAN0 ISO mode failed!")
	exit(0)
print("Set CAN0 ISO mode OK!")
ret = canDLL.ZCAN_SetCANFDStandard(m_dev,1,0)
if ret != STATUS_OK:
	print("Set CAN1 ISO mode failed!")
	exit(0)
print("Set CAN1 ISO mode OK!")

######### Second Device ############

#打开设备 
# Second device
# s_dev = canDLL.ZCAN_OpenDevice(VCI_USBCAN2, 1, 0)
# if s_dev == INVALID_DEVICE_HANDLE: 
#     print("Open Device failed!")
#     exit(0)
# print(f"Open Device OK, device handle: 0x{s_dev:x}")

#设置通道0 仲裁域波特率：1M, 数据域波特率：5M
# ret = canDLL.ZCAN_SetAbitBaud(s_dev,0,1000000)
# if ret != STATUS_OK:
# 	print("Set CAN0 abit:1M failed!")
# 	exit(0)
# print("Set CAN0 abit:1M OK!");
# ret = canDLL.ZCAN_SetDbitBaud(s_dev,0,5000000)
# if ret != STATUS_OK:
# 	print("Set CAN0 dbit:5M failed!")
# 	exit(0)
# print("Set CAN0 dbit:5M OK!");

#设置通道1 仲裁域波特率：1M, 数据域波特率：5M
# Setting buad rate: Abit 1Mbps, Dbit 5Mbps
# ret = canDLL.ZCAN_SetAbitBaud(s_dev,1,1000000)
# if ret != STATUS_OK:
# 	print("Set CAN1 abit:1M failed!")
# 	exit(0)
# print("Set CAN1 abit:1M OK!");
# ret = canDLL.ZCAN_SetDbitBaud(s_dev,1,5000000)
# if ret != STATUS_OK:
# 	print("Set CAN1 dbit:5M failed!")
# 	exit(0)
# print("Set CAN1 dbit:5M OK!");

#设置通道0,1 FDMode : ISO
# ret = canDLL.ZCAN_SetCANFDStandard(s_dev,0,0)
# if ret != STATUS_OK:
# 	print("Set CAN0 ISO mode failed!")
# 	exit(0)
# print("Set CAN0 ISO mode OK!")
# ret = canDLL.ZCAN_SetCANFDStandard(s_dev,1,0)
# if ret != STATUS_OK:
# 	print("Set CAN1 ISO mode failed!")
# 	exit(0)
# print("Set CAN1 ISO mode OK!")

######## Device 1 Configuration ########

# Config channels
init_config = ZCAN_CHANNEL_INIT_CONFIG()
init_config.can_type = TYPE_CANFD      # changed to CAN, connected to OBD (older)
init_config.config.can.mode = 0

#初始0通道
# Initializing channel 0 (dev_ch1)
dev_ch1 = canDLL.ZCAN_InitCAN(m_dev, 0, byref(init_config))
if dev_ch1 == INVALID_CHANNEL_HANDLE:
    print("Init CAN0 failed!")
    exit(0)
print("Init CAN0 OK!")

#启动通道0
# Start channel 0
ret = canDLL.ZCAN_StartCAN(dev_ch1)
if ret != STATUS_OK:
    print("Start CAN0 failed!")
    exit(0)
print("Start CAN0 OK!")	

#初始1通道
#Initializing channel 1 (dev_ch2)
# init_config.config.can.mode = 0

dev_ch2 = canDLL.ZCAN_InitCAN(m_dev, 1, byref(init_config))
if dev_ch2 == INVALID_CHANNEL_HANDLE:
    print("Init CAN1 failed!")
    exit(0)
print("Init CAN1 OK!")

######### Device 2 configuration ########

# init_config = ZCAN_CHANNEL_INIT_CONFIG()
# init_config.can_type = TYPE_CAN
# init_config.config.can.mode = 0

#初始0通道
# Initializing s_dev channel 0 (sdev_ch1)
# sdev_ch1 = canDLL.ZCAN_InitCAN(s_dev, 0, byref(init_config))
# if sdev_ch1 == INVALID_CHANNEL_HANDLE:
#     print("Init Second Device CAN0 failed!")
#     exit(0)
# print("Init Second Device CAN0 OK!")

#启动通道0
# Start s_dev channel 0
# ret = canDLL.ZCAN_StartCAN(sdev_ch1)
# if ret != STATUS_OK:
#     print("Start Second Device  CAN0 failed!")
#     exit(0)
# print("Start Second Device CAN0 OK!")	

#初始1通道
#Initializing s_dev channel 1 (sdev_ch2) but we dont need it becos we're using one channel to listen (dev_ch1)
# sdev_ch2 = canDLL.ZCAN_InitCAN(s_dev, 1, byref(init_config))
# if sdev_ch2 == INVALID_CHANNEL_HANDLE:
#     print("Init Second Device CAN1 failed!")
#     exit(0)
# print("Init Second Device CAN1 OK!")


###################################################################
#    在 ZCAN_InitCAN 之后， ZCAN_StartCAN之前配置
#	设置通道1  滤波:只接收 扩展帧,ID范围 5~6
###################################################################

## i think ch2 of device 1 (dev_ch2) is only intiated for listening, so it can start later??
canDLL.ZCAN_ClearFilter(dev_ch2)
canDLL.ZCAN_SetFilterMode(dev_ch2,0)
# canDLL.ZCAN_SetFilterStartID(dev_ch2,5)
# canDLL.ZCAN_SetFilterEndID(dev_ch2,6)

canDLL.ZCAN_AckFilter(dev_ch2)

#启动通道1
# Start channel 1
ret = canDLL.ZCAN_StartCAN(dev_ch2)
if ret != STATUS_OK:
    print("Start CAN1 failed!")
    exit(0)
print("Start CAN1 OK!")	


#################################
### CANFD frame send&&recv 
#################################
#通道1发送数据
# Channel 0 Send Messages
# transmit_canfd_num = 1
# canfd_msgs = (ZCAN_TransmitFD_Data * transmit_canfd_num)()
# for i in range(transmit_canfd_num):
# 	canfd_msgs[i].transmit_type = 1 #0=正常发送，1=单次发送，2=自发自收，3=单次自发自收。
# 	canfd_msgs[i].frame.eff     = 1 #extern frame
# 	canfd_msgs[i].frame.rtr     = 0 #remote frame
# 	canfd_msgs[i].frame.brs     = 1 #BRS is to enable faster Data Transfer Rate (Only for FD)
# 	canfd_msgs[i].frame.can_id  = i
# 	canfd_msgs[i].frame.len     = 16
# 	# for j in range(canfd_msgs[i].frame.len): #This sets it to 0x00, 0x01, 0x02...
# 	# 	canfd_msgs[i].frame.data[j] = j
     
# for j in range(canfd_msgs[i].frame.len):
#     canfd_msgs[i].frame.data[j] = 0
# ret = canDLL.ZCAN_TransmitFD(dev_ch1, canfd_msgs, transmit_canfd_num)
# print("\r\n CAN0 Tranmit CANFD Num: %d." % ret)


#通道2接收数据
#Receive Messages
# ret = canDLL.ZCAN_GetReceiveNum(dev_ch2, TYPE_CANFD)
# #print(ret)
# while ret <= 0:#如果没有接收到数据，一直循环查询接收。
#         ret = canDLL.ZCAN_GetReceiveNum(dev_ch2, TYPE_CANFD)
# if ret > 0:#接收到 ret 帧数据
# 	rcv_canfd_msgs = (ZCAN_ReceiveFD_Data * ret)()
# 	num = canDLL.ZCAN_ReceiveFD(dev_ch2, byref(rcv_canfd_msgs), ret, -1)
# 	print("CAN1 Received CANFD NUM: %d." % num)
# 	for i in range(num):
# 	    print("[%d]:ts:%d, id:%d, len:%d, eff:%d, rtr:%d, esi:%d, brs: %d, data:%s" %(
#                         i, rcv_canfd_msgs[i].timestamp, rcv_canfd_msgs[i].frame.can_id, rcv_canfd_msgs[i].frame.len,
#                         rcv_canfd_msgs[i].frame.eff, rcv_canfd_msgs[i].frame.rtr, 
#                         rcv_canfd_msgs[i].frame.esi, rcv_canfd_msgs[i].frame.brs,
#                         ''.join(str(rcv_canfd_msgs[i].frame.data[j]) + ' ' for j in range(rcv_canfd_msgs[i].frame.len))))

# def send_msg2():
#     ret = canDLL.ZCAN_TransmitFD(sdev_ch1, can_msgs2, transmit_can_num) # Sends message 2
#     print("\r\n Second Device CAN0 Tranmit CAN Num: %d." % ret)
#     return
## Testing with only one USBCAN (So multithread but with ch2 instead of a second device)
# def send_msg2_mdevch2():
#     ret = canDLL.ZCAN_TransmitFD(dev_ch2, can_msgs2, transmit_can_num) # Sends message 2
#     print("\r\n Second Channel CAN1 Tranmit CAN Num: %d." % ret)
#     return


# Message loading
import csv
import os

folder_path = 'C:/Users/Zu Kai/astar_git/OBD2/output_parameters_DID'
files = os.listdir(folder_path) #create a list of files in the folder
param_dict = {}

for index, file in enumerate(files):
    print(f"{index}: {file}")
manufacturer = files[int(input('Choose Manufacturer by Index: \n'))]
folder_path = f'{folder_path}/{manufacturer}'

files = os.listdir(folder_path)
for index, file in enumerate(files):
    print(f"{index}: {file}")
model = files[int(input('Choose Model by Index: \n'))]

filepath = f'{folder_path}/{model}'

with open(f'{filepath}', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        param_name = row['Parameter']  # Ensure this matches your CSV header
        can_id = row['CAN_ID']
        param_dict[param_name] = {
             'can_id':can_id,
             'payload':row['UDS Request Payload']  # Entire row as the value
            }
# iternary = [print(f'{key[4:]}') for key in param_dict.keys()]

keys_list = list(param_dict.keys()) # Get the keys (Parameters) in list

for index, key in enumerate(keys_list):
    print(f"{index}: {key}")

# Validation Loop
def valid_loop():
     i = True
     while i:
        query_index = int(input("Choose the index of the parameter you want to query:\n"))
        
        if query_index in range(0, len(keys_list)):
            parameter = keys_list[query_index] # Get the key for the selected index

            try:
                payload = param_dict[parameter]["payload"]
            except Exception:
                print(f"Missing payload for {manufacturer} {model}'s {parameter}")
            try:
                did = int(param_dict[parameter]["can_id"], 16)
            except Exception:
                print(f"Missing CAN ID for {manufacturer} {model}'s {parameter}") 
            else:
                i = False
                return parameter, payload, did
        else:
            print("Invalid index. Please choose again.")
            
            
parameter, payload, did = valid_loop()
databytes = payload.split()
byte_list = [int(b, 16) for b in payload.strip().split()]
print(byte_list)


#################################
### CAN frame send&&recv
#################################
#通道1发送数据
transmit_can_num = 1
can_msgs = (ZCAN_Transmit_Data * transmit_can_num)()
for i in range(transmit_can_num):
    can_msgs[i].transmit_type = 0 #0=正常发送，1=单次发送，2=自发自收，3=单次自发自收。
    can_msgs[i].frame.eff     = 0 #extern frame
    can_msgs[i].frame.rtr     = 0 #remote frame
    # can_msgs[i].frame.brs     = 0 #BRS 
    can_msgs[i].frame.can_id  = did
    can_msgs[i].frame.can_dlc = 8

    can_msgs[i].frame.data = ( c_ubyte * 8 )(*byte_list)
    # print(type(can_msgs[i].frame.data))

    # for j in range(can_msgs[i].frame.can_dlc):
    #     can_msgs[i].frame.data[j] = j
#     for j in range(can_msgs[i].frame.can_dlc):
#         can_msgs[i].frame.data[j] = 0
# ret = canDLL.ZCAN_Transmit(dev_ch1, can_msgs, transmit_can_num)
# print("\r\nCAN0 Transmit CAN Num: %d." % ret)

#### Flow control Message ####
flow_bytelist = [0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
flow_msg = (ZCAN_Transmit_Data * 1)()
flow_msg[0].transmit_type = 0 #0=正常发送，1=单次发送，2=自发自收，3=单次自发自收。
flow_msg[0].frame.eff     = 0 #extern frame
flow_msg[0].frame.rtr     = 0 #remote frame
# can_msgs[i].frame.brs     = 0 #BRS 
flow_msg[0].frame.can_id  = did
flow_msg[0].frame.can_dlc = 8
flow_msg[0].frame.data = ( c_ubyte * 8 )(*flow_bytelist)


def send_msg1():
    ret = canDLL.ZCAN_Transmit(dev_ch1, can_msgs, transmit_can_num) # Sends message 1
    print("\r\nSend MSG CAN0 Transmit CAN Num: %d." % ret)
    print(f"\nSending payload request for {parameter}: {payload}")
    # for msg in can_msgs:
    #      print(type(msg))
    # print("\r\n CAN0 Transmit CAN msg: %d." % can_msgs[0].frame.data[0])
    return ret

ret = send_msg1();

#通道2接收数据
#Receive Messages
# ret = canDLL.ZCAN_GetReceiveNum(dev_ch2, TYPE_CAN)
# print(ret)
print("Receiving...")
print("ret: %s" % ret)
# def receive_msg1(ret):
# rcv_can_msgs = (ZCAN_Receive_Data * 10)()
# print(''.join(str(rcv_can_msgs[0].frame.data[j]) + ' ' for j in range(rcv_can_msgs[0].frame.can_dlc)))

def receive_msg():
    ret = canDLL.ZCAN_GetReceiveNum(dev_ch2, TYPE_CAN)

    counter = 0
    while ret <= 0:#如果没有接收到数据，一直循环查询接收。
            ret = canDLL.ZCAN_GetReceiveNum(dev_ch2, TYPE_CAN)
            time.sleep(0.5)
            counter += 1
            print("counter: %s" % counter)
            # if counter > 10:
            #     break
    if ret > 0:#接收到 ret 帧数据
        rcv_can_msgs = (ZCAN_Receive_Data * ret)()
        num = canDLL.ZCAN_Receive(dev_ch2, byref(rcv_can_msgs), ret, -1)
        print("CAN1 Received CAN NUM: %d." % num)
        for i in range(num):
            print("[%d]:ts:%d, id:%X, len:%d, eff:%d, rtr:%d, data:%s" %(
                            i, rcv_can_msgs[i].timestamp, rcv_can_msgs[i].frame.can_id, rcv_can_msgs[i].frame.can_dlc,
                            rcv_can_msgs[i].frame.eff, rcv_can_msgs[i].frame.rtr,                         
                            ''.join(f'{rcv_can_msgs[i].frame.data[j]:02x} ' for j in range(rcv_can_msgs[i].frame.can_dlc))))
        

        # print("[%d]:ts:%d, id:%d, len:%d, eff:%d, rtr:%d, data:%s" %(
        #                 1, rcv_can_msgs[1].timestamp, rcv_can_msgs[1].frame.can_id, rcv_can_msgs[1].frame.can_dlc,
        #                 rcv_can_msgs[1].frame.eff, rcv_can_msgs[1].frame.rtr,                         
        #                 ''.join(str(rcv_can_msgs[1].frame.data[j]) + ' ' for j in range(rcv_can_msgs[1].frame.can_dlc))))

def receive_msg_flowcontrol():
    ret = canDLL.ZCAN_GetReceiveNum(dev_ch2, TYPE_CAN)

    counter = 0
    while ret <= 0:#如果没有接收到数据，一直循环查询接收。
            ret = canDLL.ZCAN_GetReceiveNum(dev_ch2, TYPE_CAN)
            time.sleep(0.5)
            counter += 1
            print("counter: %s" % counter)
            # if counter > 10:
            #     break
    if ret > 0:#接收到 ret 帧数据
        rcv_can_msgs = (ZCAN_Receive_Data * ret)()
        num = canDLL.ZCAN_Receive(dev_ch2, byref(rcv_can_msgs), ret, -1)
        print("CAN1 Received CAN NUM: %d." % num)
        for i in range(num):
            print("[%d]:ts:%d, id:%X, len:%d, eff:%d, rtr:%d, data:%s" %(
                            i, rcv_can_msgs[i].timestamp, rcv_can_msgs[i].frame.can_id, rcv_can_msgs[i].frame.can_dlc,
                            rcv_can_msgs[i].frame.eff, rcv_can_msgs[i].frame.rtr,                         
                            ''.join(f'{rcv_can_msgs[i].frame.data[j]:02x} ' for j in range(rcv_can_msgs[i].frame.can_dlc))))
            
        # After confirmation of receiving First Frame
        # time.sleep(1)
        fc = canDLL.ZCAN_Transmit(dev_ch1, flow_msg, 1) # Sends message 1
        print("\r\nTransmitting Flow control Message...\n: %d." % fc)
        time.sleep(0.5)
        rcv_can_msgs = (ZCAN_Receive_Data * ret)()
        num = canDLL.ZCAN_Receive(dev_ch2, byref(rcv_can_msgs), ret, -1)
        print("CAN1 Received CAN NUM (Flow Control): %d." % num)
        for i in range(num):
            print("[%d]:ts:%d, id:%X, len:%d, eff:%d, rtr:%d, data:%s\n" %(
                            i, rcv_can_msgs[i].timestamp, rcv_can_msgs[i].frame.can_id, rcv_can_msgs[i].frame.can_dlc,
                            rcv_can_msgs[i].frame.eff, rcv_can_msgs[i].frame.rtr,                         
                            ''.join(f'{rcv_can_msgs[i].frame.data[j]:02x} ' for j in range(rcv_can_msgs[i].frame.can_dlc))))

time.sleep(1) # give time for transmission
receive_msg_flowcontrol()


### multithreading setup ###
import threading

# thread1 = threading.Thread(target=send_msg1)
# # thread2 = threading.Thread(target=send_msg2)
# # thread2 = threading.Thread(target=send_msg2_mdevch2)

# thread2 = threading.Thread(target=receive_msg1())


# thread1.start()
# thread2.start() 

# time.sleep(20)
# thread1.join()
# thread2.join()





#关闭
ret = canDLL.ZCAN_ResetCAN(dev_ch1)
if ret != STATUS_OK:
    print("Close CAN0 failed!")
    exit(0)
print("Close CAN0 OK!")	

ret = canDLL.ZCAN_ResetCAN(dev_ch2)
if ret != STATUS_OK:
    print("Close CAN1 failed!")
    exit(0)
print("Close CAN1 OK!")	

ret = canDLL.ZCAN_CloseDevice(m_dev) 
if ret != STATUS_OK:
    print("Close Device failed!")
    exit(0)
print("Close Device OK!")

