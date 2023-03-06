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
    12: "CIO3" #S11 CIO3
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
