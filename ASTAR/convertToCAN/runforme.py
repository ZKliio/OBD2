import os
from udsToCANjeju import main # CSV UDS to can
from udsToCAN import main as main1# JSON UDS to can
input_sets = [
    ["0", "0"],
    ["0", "1"],
    ["0", "2"],
    ["0", "3"],
    ["1", "0"],
    ["1", "1"],
    ["1", "2"],
    ["1", "3"],
    ["1", "4"],
    ["1", "5"],
    ["1", "6"],
    ["1", "7"],
]

source_list = [
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Ioniq%20EV%20-%2028kWh",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Ioniq%20HEV",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Ioniq%20PHEV%20-%208.9kWh",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Hyundai%20Kona%20EV%20%26%20Kia%20Niro%20EV",

    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Hyundai%20Kona%20EV%20%26%20Kia%20Niro%20EV",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Kia%20Niro%20HEV",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Kia%20Niro%20PHEV%20-%208.9kWh",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Optima%20PHEV%20-%209.8kWh",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Ray%20EV",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Soul%20EV%20-%2027kWh",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Soul%20EV%20-%2030kWh",
    "https://github.com/JejuSoul/OBD-PIDs-for-HKMC-EVs/tree/master/Soul%20EV%20-%2064kWh",
]

source_list_json = [
    "https://github.com/iternio/ev-obd-pids/blob/main/ford/MachE.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/gmc/bolt17.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/gmc/bolt19.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/hkmc/hkmc2017.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/hkmc/hkmc2019.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/jaguar/ipace2019.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/jaguar/ipace2021.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/mg/mgzsev.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/renault/zoe.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/renault/zoe2.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/volkswagen/eGolf.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/volkswagen/eUP.json",
    "https://github.com/iternio/ev-obd-pids/blob/main/volkswagen/MEB.json",
]

input_sets_json = [
    ["0", "0"],
    ["1", "0"],
    ["1", "1"],
    ["2", "0"],
    ["2", "1"],
    ["3", "0"],
    ["3", "1"],
    ["4", "0"],
    ["5", "0"],
    ["5", "1"],
    ["6", "0"],
    ["6", "1"],
    ["6", "2"],
    
]

# Manual Mode
# def mock_input(prompt=None):
#     return input()
# main1(mock_input, sourcelink=None)

def mock_input(prompt):
    print("Entering prompt:", prompt)   
    return next(inputs)

i = 0

# *********CSV*********
# Run main() with each set of inputs
# for input_values in input_sets:
#     inputs = iter(input_values)
#     # input = mock_input  # Override built-in input (doesnt work due to local vs global scope)
#     main(mock_input, sourcelink=source_list[i])
#     i+=1

# *********JSON*********
# Run main() with each set of inputs
for input_values in input_sets_json:
    inputs = iter(input_values)
    # input = mock_input  # Override built-in input (doesnt work due to local vs global scope)
    main1(mock_input, sourcelink=source_list_json[i])
    i+=1