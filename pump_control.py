"""
Here we will control the motors/pumps
Each pump/motor will be assigned to a specific chemical, done during station preparation.( see station_preparation.py)

1. Pick a buffer to be made. ( The buffer will have a list of chemicals to be made)
2. Prompt the user to adjustment the individual chemical weight.
if the choice is yes then add the additional weight to the chemicals total weight
if the users choice is no, then the target weight remains to be the solvent target weight = buffer weight

Run each motor/pump one by one till the required target is reached

"""

#import RPi.GPIO as GPIO
import time
import mysql.connector
#import station_preparation
#from station_preparation import *

# Connect to the database
buffer_mix_db = mysql.connector.connect(
  host="localhost", #"localhost",
  user="phdd",  #"yourusername",
  password="root",  # "yourpassword",
  database="BufferStationDB", #"yourdatabase"
)

#Creating a cursor object using the cursor() method
mycursor = buffer_mix_db.cursor()

mycursor.execute("USE BufferStationDB")
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

buffer_choice = int(input("Enter the number of the buffer you want to use: "))
selected_buffer_name = buffers[buffer_choice - 1][0]

# Get the chemicals and their respective pump numbers for the selected buffer
mycursor.execute("SELECT b.buffer_name, c.chemName, c.pumpNo FROM solventmix bc "
                 "JOIN buffers b ON bc.buffer_id = b.buffer_id "
                 "JOIN chemicals c ON bc.chem_id = c.chemID "
                 "WHERE b.buffer_name = %s", (selected_buffer_name,))
chemBuff_results = mycursor.fetchall()

# Print the results
if chemBuff_results:
    print("Below are the chemicals and pumps for Buffer:{}".format(selected_buffer_name))
    for result in chemBuff_results:
        print(f"{result[1]} connected to - Pump {result[2]}")
else:
    print("No chemicals found for buffer {}".format(selected_buffer_name))


# """
# # Prompt the user to adjust the individual chemical weights
# chemical_weights = {}
# for i in range(1, 13):
#     chemical_name = selected_buffer[i * 2]
#     chemical_weight = selected_buffer[(i * 2) + 1]
#     adjust_weight = input("Adjust weight for {}: {} g (y/n)? ".format(chemical_name, chemical_weight))
#     if adjust_weight.lower() == "y":
#         additional_weight = float(input("Enter additional weight (in g): "))
#         chemical_weight += additional_weight
#     chemical_weights[chemical_name] = chemical_weight
#
# # Calculate the total weight of the buffer
# total_weight = sum(chemical_weights.values())
#
# # Prompt the user to confirm the buffer details
# print("Buffer: {}".format(selected_buffer[0]))
# print("Total weight: {} g".format(total_weight))
# for chemical, weight in chemical_weights.items():
#     print("{}: {} g".format(chemical, weight))
# confirm = input("Confirm buffer details (y/n)? ")
# if confirm.lower() != "y":
#     print("Buffer creation cancelled.")
#     exit()
#
#
# # Update the actual weight in the solventmixer table
# mycursor.execute("UPDATE solventmixer SET actual_weight = %s WHERE solvent_name = %s",
#                  (total_weight, selected_buffer[0]))
# buffer_mix_db.commit()
# print("Solvent mixer updated with actual weight.")
#
# """
