"""
Here we will control the motors/pumps
Each pump/motor will be assigned to a specific chemical, done during station preparation.( see station_preparation.py)

Run each motor/pump one by one till the required chemical weight target is reached

"""

import time
from labjack import ljm
#---------------- PHASE 00 -MAKE SURE THERE IS CONNECTION to the Labjack  ------------------------------#

mylabjack = ljm.openS("ANY", "ANY","ANY") #Connect to any labkjack connected to the host computer or network
info = ljm.getHandleInfo(mylabjack)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
      "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
      (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))
################ End of the connected Labjack info ####################

# Specify the pins for each pump
pump_pins = {
    #P1 - DB15 connector
    1: "EIO0", #S0 	EIO0  
    2: "EIO1", #S1 	EIO1
    3: "EIO2", #S2 	EIO2
    4: "EIO3", #S3 	EIO3
    5: "EIO4", #S4 	EIO4
    6: "EIO5", #S5 	EIO5
    7: "EIO6", #S6 	EIO6
    8: "EIO7", #S7 	EIO7
    9: "CIO0", #S8 	CIO0
    10: "CIO1",#S9 	CIO1
    11: "CIO2",#S10 CIO2
    12: "CIO3", #S11 CIO3
#P2 - DB37 connector
    13: "FIO0", #S0 FIO0  
    14: "FIO1", #S1 FIO1
    15: "FIO2", #S2 FIO2
    16: "FIO3", #S3 FIO3
    17: "FIO4", #S4 FIO4
    18: "FIO5", #S5 FIO5
    19: "FIO6", #S6 FIO6
    20: "FIO7", #S7 FIO7
    21: "DAC0", #S8 DAC0
    22: "DAC1", #S9 DAC1
    23: "MIO0", #S10 MIO0
    24: "MIO1"  #S11 MIO1
}

# Set each pump pin high
for pump_num, pin_name in pump_pins.items():
    ljm.eWriteName(mylabjack, pin_name, 1) # Set the pin high
    print(f"Set pump {pump_num} pin {pin_name} high")
    time.sleep(3) # Wait for 1 second

# Set each pump pin low
for pump_num, pin_name in pump_pins.items():
    ljm.eWriteName(mylabjack, pin_name, 0) # Set the pin low
    print(f"Set pump {pump_num} pin {pin_name} low")
    time.sleep(1) # Wait for 1 second

# Close the Labjack connection
ljm.close(mylabjack)
