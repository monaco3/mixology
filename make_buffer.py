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

buffer_choice = int(input("Enter the buffer number you want to use: "))
selected_buffer_name = buffers[buffer_choice - 1][0]

# Get the chemicals and their respective pump numbers for the selected buffer
mycursor.execute("SELECT b.buffer_name, c.chemName,c.pumpNo, c.molarWeight FROM solventmix bc "
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

# Loop through each chemical used in the buffer and insert its data into the processedBuffer table
for result in chemBuff_results:
    chemical_name = result[1]
    original_weight = result[3]
    adjusted_weight = chemical_weights[chemical_name]
    mycursor.execute("SELECT chemID FROM chemicals WHERE chemName = %s", (chemical_name,))
    chem_id = mycursor.fetchone()[0]
    data = (nameofbuffer_processor, batch_number, buffer_id, chem_id, original_weight, adjusted_weight)
    mycursor.execute(processedBuffer_sql, data)

# Commit the changes to the database
buffer_mix_db.commit()

# Print a success message
print("Buffer creation successful. Data saved to processedBuffer table.")
