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


#
# # Populate the buffer_chemicals table
# mycursor.execute("SELECT buffer_id, chemical_1, chemical_2, chemical_3, chemical_4, chemical_5, chemical_6, chemical_7, chemical_8, chemical_9, chemical_10, chemical_11, chemical_12 FROM buffers")
# buffers = mycursor.fetchall()
#
# for buffer in buffers:
#     buffer_id = buffer[0]
#     for i in range(1, 13):
#         chem_name = buffer[i]
#         if chem_name:
#             mycursor.execute("SELECT chemID FROM chemicals WHERE chemName = %s", (chem_name,))
#             chem_id = mycursor.fetchone()[0]
#             mycursor.execute("INSERT INTO buffer_chemicals (buffer_id, chem_id) VALUES (%s, %s)", (buffer_id, chem_id))
#
# # Commit the changes to the database
# buffer_mix_db.commit()
#
# # Close the cursor and database connections
# mycursor.close()
# buffer_mix_db.close()




# Prompt user to select a buffer
buffer_name = input("Enter the name of the buffer you want to make: ")

# Get the chemicals and their respective pump numbers for the selected buffer
mycursor.execute("SELECT b.buffer_name, c.chemName, c.pumpNo FROM buffer_chemicals bc "
                 "JOIN buffers b ON bc.buffer_id = b.buffer_id "
                 "JOIN chemicals c ON bc.chem_id = c.chemID "
                 "WHERE b.buffer_name = %s", (buffer_name,))
results = mycursor.fetchall()

# Print the results
if results:
    print(f"Chemicals and their respective pump numbers for buffer '{buffer_name}':")
    for result in results:
        print(f"{result[1]} - Pump {result[2]}")
else:
    print(f"No chemicals found for buffer '{buffer_name}'.")

















# Prompt the user to select a buffer
# print("Select a buffer from the following list:")
# mycursor.execute("SELECT buffer_name FROM buffers")
# buffers = mycursor.fetchall()
# for i, buffer in enumerate(buffers):
#     print("{} - {}".format(i+1, buffer[0]))
#
# buffer_choice = int(input("Enter the number of the buffer you want to use: "))
# selected_buffer_name = buffers[buffer_choice - 1][0]
#
# # Retrieve the list of chemicals and their pump numbers
# mycursor.execute("SELECT * FROM buffers WHERE buffer_name = %s", (selected_buffer_name,))
# selected_buffer = mycursor.fetchone()
#
# #print(selected_buffer[i * 1])
#
# chemical_pumps = {}
# for i in range(1, 13):
#     chemical_name = selected_buffer[i * 1]
#     if chemical_name is None:
#         break
#     mycursor.execute("SELECT pumpNo FROM chemicals WHERE chemName = %s", (chemical_name,))
#     pump_number = mycursor.fetchone()[1]
#     chemical_pumps[chemical_name] = pump_number
#
# print("The following chemicals are in the {} buffer:".format(selected_buffer_name))
# for chemical_name, pump_number in chemical_pumps.items():
#     print("- {} (pump {})".format(chemical_name, pump_number))
#
#
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
