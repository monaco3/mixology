import time
from labjack import ljm
#---------------- PHASE 00 -MAKE SURE THERE IS CONNECTION ------------------------------#
################ Get information of connected Labjack ####################
handle = ljm.openS("ANY", "ANY","ANY") #Connect to the labjack to any labkjack connected to the host computer or network
info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
      "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
      (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))
################ End of the connected Labjack info ####################

# import the LabJack library
import labjack

# Setup and call eReadAddress to read a value from the Labjack
address = 2018  #Adress for CIO2 where the motor is connected this can be checked in the register matrix in kipling
# name = CIO2

dataType = ljm.constants.UINT16

liquid_level = 0 # 24 volts
change_by = 0.5

while True:



    if liquid_level !=24 :
        change_by += change_by

    change_by  = change_by + change_by

    print("You have reached the desired level")
    ljm.eWriteAddress(handle, address, dataType, change_by)

    # result_name = ljm.eReadName(handle, name)

    print("\neWriteAddress: ")
    print("   Address -%i, data type -%i, value : %f" % (address, dataType, change_by))

    time.sleep(3)  # Sleep for 3 seconds to allopw nough time for the voltage to stabalize

# Close the handle to end processing
ljm.close(handle)
# def mix_liquids(liquid1, liquid2, liquid3, liquid4, liquid5):
#     total_volume = sum([liquid1, liquid2, liquid3, liquid4, liquid5])
#     if total_volume == 1000:
#         return "You have already reached 1 litre, no mixing needed."
#     elif total_volume > 1000:
#         return "You have exceeded 1 litre, please adjust the amount of liquids."
#     else:
#         # Mix the liquids to reach 1 litre
#         mixture = []
#         mixture.append(liquid1 / total_volume)
#         mixture.append(liquid2 / total_volume)
#         mixture.append(liquid3 / total_volume)
#         mixture.append(liquid4 / total_volume)
#         mixture.append(liquid5 / total_volume)
#
#         # Normalize the mixture to reach 1 litre
#         mixture = [x * 1000 for x in mixture]
#         return mixture
#
# # Example usage
# liquids = [200, 300, 250, 150, 100]
# print(mix_liquids(*liquids))