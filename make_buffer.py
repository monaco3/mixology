"""
1. Pick a buffer to be made. ( The buffer will have a list of chemicals to be made)
2. Prompt the user to adjust the individual chemical weight.
if the choice is yes then add the additional weight to the chemicals total weight
if the users choice is no, then the target weight remains to be the solvent target weight = buffer weight
"""

import time
import mysql.connector
#import station_preparation
#from station_preparation import *

# Connect to the database
buffer_mix_db = mysql.connector.connect(
  host="sql7.freesqldatabase.com", #"localhost",
  user="sql7606170",  #"yourusername",
  password="X74Xryppcr",  # "yourpassword",
  database="sql7606170", #"yourdatabase"
  port="3306",
)

import time
from labjack import ljm
#---------------- PHASE 00 -MAKE SURE THERE IS CONNECTION to the Labjack  ------------------------------#

mylabjack = ljm.openS("ANY", "ANY","ANY") #Connect to any labkjack connected to the host computer or network
info = ljm.getHandleInfo(mylabjack)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
       "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
       (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))
# ################ End of the connected Labjack info ####################

#Creating a cursor object using the cursor() method
mycursor = buffer_mix_db.cursor()

mycursor.execute("USE sql7606170")
buffer_mix_db.commit()
#mycursor.execute("DROP TABLE buffer_chemicals")


# Prompt user to select a buffer
#buffer_name = input("Enter the name of the buffer you want to make: ")

#Prompt the user to select a buffer
print("Select a buffer from the following list:")
mycursor.execute("SELECT buffer_name FROM buffers")
buffers = mycursor.fetchall()
for i, buffer in enumerate(buffers):
    print("{} - {}".format(i+1, buffer[0]))

buffer_choice = int(input("Enter the buffer number you want to use: "))
selected_buffer_name = buffers[buffer_choice - 1][0]

# Get the chemicals and their respective pump numbers for the selected buffer
mycursor.execute("SELECT b.buffer_name, c.chemName,c.pumpNo, c.molarWeight FROM solventmix bc "
                 "JOIN buffers b ON bc.buffer_id = b.buffer_id "
                 "JOIN chemicals c ON bc.chem_id = c.chemID "
                 "WHERE b.buffer_name = %s", (selected_buffer_name,))
chemBuff_results = mycursor.fetchall()


class UsedPumps:
    def __init__(self):
        self.pumps = set()

    def add_pump(self, pump_number):
        self.pumps.add(pump_number)

    def remove_pump(self, pump_number):
        self.pumps.remove(pump_number)

    def get_pumps(self):
        return sorted(self.pumps)


# Create an instance of the UsedPumps class
used_pumps = UsedPumps()

# Print the results
if chemBuff_results:
    print("Below are the chemicals and pumps for Buffer:{}".format(selected_buffer_name))
    for result in chemBuff_results:
        print(f"{result[1]} connected to - Pump {result[2]}")
        used_pumps.add_pump(result[2])
    print("Pumps used: {}".format(used_pumps.get_pumps()))
else:
    print("No chemicals found for buffer {}".format(selected_buffer_name))


#Connect the pumps to corresponding labjack pins

# Specify the pins for each pump
pump_pins = {
    1: "EIO6", #S0 	EIO0
    2: "EIO7", #S1 	EIO1
    3: "EIO4", #S2 	EIO2
    4: "EIO3", #S3 	EIO3
    5: "EIO4", #S4 	EIO4
    6: "CIO3", #S5 	EIO5
    7: "EIO6", #S6 	EIO6
    8: "EIO7", #S7 	EIO7
    9: "CIO0", #S8 	CIO0
    10: "CIO1",#S9 	CIO1
    11: "CIO2",#S10 CIO2
    12: "EIO5" #S11 CIO3
}

# Link the used pumps to the motor pins
#pumps_used = used_pumps.get_pumps()
motor_pins = []
for pump in used_pumps.get_pumps():
    if pump in pump_pins:
        motor_pins.append(pump_pins[pump])

# Print the motor pins used
print("Motor pins used: {}".format(", ".join(motor_pins)))

###----ADJUSTING THE CHEMICAL VALUES FOR THE SELECTED BUFFER--------------

# Prompt the user to adjust the individual chemical weights
chemical_weights = {}
for result in chemBuff_results:
    chemical_name = result[1]
    chemical_weight = result[3]
    adjust_weight = input("Adjust weight for {}: {} g (YES/NO)? ".format(chemical_name, chemical_weight))
    if adjust_weight.lower() == "yes":
        additional_weight = float(input("Enter the weight you want to add (in g): "))
        chemical_weight += additional_weight
    chemical_weights[chemical_name] = chemical_weight

# Calculate the total weight of the buffer
new_chemical_weight = sum(chemical_weights.values())

# Prompt the user to confirm the buffer details
print("Buffer: {}".format(selected_buffer_name))
print("Total weight for {} is : {} g".format(selected_buffer_name, new_chemical_weight))
for chemical, weight in chemical_weights.items():
    print("{}: {} g".format(chemical, weight))
confirm = input("Confirm buffer details (YES/NO)? ")
if confirm.lower() != "yes":
    print("Buffer creation cancelled.")
    exit()

# Prompt the user to enter the buffer_processor_name and batch_number
nameofbuffer_processor = input("Enter your initials or name: ")
batch_number = input("Enter the batch_number: ")

# Get the buffer_id for the selected buffer name
mycursor.execute("SELECT buffer_id FROM buffers WHERE buffer_name = %s", (selected_buffer_name,))
buffer_id = mycursor.fetchone()[0]

# Prepare the SQL statement to insert the processed buffer data
processedBuffer_sql = "INSERT INTO processedBuffer (nameofbuffer_processor, batch_number, buffer_id, chem_id, original_weight, adjusted_weight) VALUES (%s, %s, %s, %s, %s, %s)"

#
# # Loop through each chemical used in the buffer and insert its data into the processedBuffer table
# for result in chemBuff_results:
#     chemical_name = result[1]
#     original_weight = result[3]
#     adjusted_weight = chemical_weights[chemical_name]
#     mycursor.execute("SELECT chemID FROM chemicals WHERE chemName = %s", (chemical_name,))
#     chem_id = mycursor.fetchone()[0]
#     data = (nameofbuffer_processor, batch_number, buffer_id, chem_id, original_weight, adjusted_weight)
#     mycursor.execute(processedBuffer_sql, data)



# Loop through each chemical used in the buffer and insert its data into the processedBuffer table
for result in chemBuff_results:
    chemical_name = result[1]
    original_weight = result[3]
    adjusted_weight = chemical_weights[chemical_name]
    mycursor.execute("SELECT chemID FROM chemicals WHERE chemName = %s", (chemical_name,))
    chem_id = mycursor.fetchone()[0]
    data = (nameofbuffer_processor, batch_number, buffer_id, chem_id, original_weight, adjusted_weight)
    mycursor.execute(processedBuffer_sql, data)

    # Calculate the duration for how long the motor pin should be turned high based on the adjusted weight
    duration = int(round(adjusted_weight * 1000))

    # Print the adjusted weight and the duration
    print(f"{chemical_name}: adjusted weight = {adjusted_weight}, duration = {duration}ms")

    # Turn the motor pin high for the specified duration
    pump_number = result[2]
    pin = pump_pins[pump_number]
    #daq.setDigitalPin(pin, 1)
    ljm.eWriteName(mylabjack, pin, 1)  # Set the pin high
    print(f"Set pin {pin} high")
    time.sleep(duration/10000)
    #time.sleep(2)
    #daq.setDigitalPin(pin, 0)
    ljm.eWriteName(mylabjack, pin, 0)  # Set the pin low
    print(f"Set pin {pin} low")

    # Add the pump to the set of used pumps
    used_pumps.add_pump(pump_number)

# Print the list of used pumps
print("Pumps used: {}".format(used_pumps.get_pumps()))




#     # Control the LabJack to dispense the chemical
#     duration = int(adjusted_weight * 1)  # Convert weight to milliseconds
#     ljm.eWriteName(mylabjack, pin_number, 1)  # Set the pin high
#     print(f"Set pin {pin_number} high")
#     time.sleep( duration )  # Wait for the duration of the dispense
#
#     # Set the pump pin low
#     ljm.eWriteName(mylabjack, pin_number, 0)  # Set the pin low
#     print(f"Set pin {pin_number} low")
#
# # Close the Labjack connection
# ljm.close(mylabjack)

# Commit the changes to the database
buffer_mix_db.commit()

# Print a success message
print("Buffer creation successful. Data saved to processedBuffer table.")





