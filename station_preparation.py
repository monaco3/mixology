"""
Here we prepare the chemicals that need to be used and assign them to a specific pump.
- Create a Chemical table and add Chemical details

We then Create a buffer with various chemicals. Buffer can only be made by selecting from the available chemicals
- Create a buffer table and pick which chemicals to add. Include desired weight/volume of each buffer


"""
from database_setup import*
import mysql.connector
#
# # Establishing a connection to the database
# try:
#     buffer_mix_db = mysql.connector.connect(
#         host="localhost",
#         user="phdd",
#         password="root",
#         database="BufferStationDB",
#     )
#     print("Connection established successfully!")
# except mysql.connector.Error as error:
#     print(f"Error connecting to MySQL: {error}")

#Creating a cursor object using the cursor() method
mycursor = buffer_mix_db.cursor()

#Retrieving the list of tables print("List of tables in the database: ")
#This is a test to be sure database_setup.py import works
mycursor.execute("SHOW Tables")
print(mycursor.fetchall())





##------ENTERING THE CHEMICAL LIST INTO CHEMICALS TABLE--------------

# Loop to prompt the user to enter chemical details
while True:
  #Prompt the user to enter the chemical details
  chemName = input("Enter the chemical name: ")
  addedAmount = float(input("Enter the added amount of the Chemical in grams: "))
  molarWeight = float(input("Enter the Molar weight in grams/mole: "))
  pumpNo = input("Enter the pump number (Pump 1-12): ")

  # Insert the chemical details into the database
  mycursor.execute("INSERT INTO chemicals (chemName, addedAmount, molarWeight, pumpNo) VALUES (%s, %s, %s, %s)", (chemName, addedAmount, molarWeight, pumpNo))
  buffer_mix_db.commit()

  # Print a message to confirm the insertion
  print("{} added to the database.".format(chemName))

  # Ask the user if they want to continue entering chemicals
  choice = input("Do you want to enter another chemical? (YES/NO): ")
  if choice.lower() != "yes":
    break
print("You have finished logging chemicals into the database/system")




##------MAKING OF BUFFER - INTO BUFFERS TABLE--------------
# Here we prompt the user to select chemicals from the list and add them to the buffer
# Get a list of all chemicals from the chemicals table
mycursor.execute("SELECT chemName FROM chemicals")
chemicals_list = [a_chem [0] for a_chem in mycursor.fetchall()]

# Initialize/create a buffer dictionary
buffer_dict = {}

while True:
  # Display the list of chemicals to the user
  print("The Available chemicals are:")
  for i, chem in enumerate(chemicals_list):
    print(f"{i + 1}. {chem}")

  # Prompt the user to select a chemical
  chem_choice = int(input("Enter the number of the chemical you want to add to the buffer: "))
  chem_name = chemicals_list[chem_choice - 1]
  chem_weight = float(input("Enter the weight of the chemical in grams: ")) #Weight of the chem needed for the buffer

  # Add the chemical and its weight to the buffer dictionary
  buffer_dict[chem_name] = chem_weight

  # Ask the user if they want to add more chemicals to the buffer if they answe no, break out of loop
  choice = input("Do you want to add another chemical to the buffer? (YES/NO): ")
  if choice.lower() != "yes":
    break

# Insert the buffer into the buffer table
buffer_name = input("Enter a name for the buffer: ")
buffer_maker = input("Enter Your User Initials: ")
buffer_weight = sum(buffer_dict.values())
buffer_values = [buffer_name,buffer_maker, buffer_weight]
for chem_name, chem_weight in buffer_dict.items():
  buffer_values.append(chem_name)
  buffer_values.append(chem_weight)

# Insert the buffer values into the buffer table
buffer_query = "INSERT INTO buffers (buffer_name,buffer_maker, buffer_weight"
for i in range(1, len(buffer_dict) + 1):
  buffer_query += f", chemical_{i}, chemical_{i}_weight"
buffer_query += ") VALUES ("
for i in range(len(buffer_values)):
  if isinstance(buffer_values[i], str):
    buffer_query += f"'{buffer_values[i]}'"
  else:
    buffer_query += str(buffer_values[i])
  if i < len(buffer_values) - 1:
    buffer_query += ", "
buffer_query += ")"
mycursor.execute(buffer_query)
buffer_mix_db.commit()

print("Your Buffer has been added to the buffer list.")

##------------------------POPULATING THE JOINING TABLE--TAKES CARE OF RELATIONSHIP-----------
# Populate the solventmix table so that once the buffer is made the solventmix is also automatically populated
#This table is an intermediate many to many relationsip table connecting chemiacals and buffer tables
mycursor.execute("SELECT buffer_id, buffer_maker, chemical_1, chemical_2, chemical_3, chemical_4, chemical_5, chemical_6, chemical_7, chemical_8, chemical_9, chemical_10, chemical_11, chemical_12 FROM buffers")
buffers = mycursor.fetchall()

for buffer in buffers:
    buffer_id = buffer[0]
    buffer_maker = buffer[1]
    for i in range(2, 14):
        chem_name = buffer[i]
        if chem_name:
            mycursor.execute("SELECT chemID FROM chemicals WHERE chemName = %s", (chem_name,))
            chem_id = mycursor.fetchone()[0]
            mycursor.execute("INSERT INTO solventmix (buffer_id, chem_id, buffer_maker) VALUES (%s, %s, %s)", (buffer_id, chem_id, buffer_maker))

# Commit the changes to the database
buffer_mix_db.commit()





"""
# Prompt the user to select a buffer from the buffer table
print("Select a buffer from the following list:")
mycursor.execute("SELECT buffer_name, buffer_weight FROM buffers")
buffers = mycursor.fetchall()
for i, buffer in enumerate(buffers):
    print("{} - {} ({} g)".format(i+1, buffer[0], buffer[1]))

buffer_choice = int(input("Enter the number of the buffer you want to use: "))
selected_buffer = buffers[buffer_choice - 1]

# Prompt the user to enter the solvent details
solvent_name = input("Enter the solvent name: ")
batch_number = input("Enter the batch number: ")
target_weight = selected_buffer[1]

# Insert the solvent details into the database
mycursor.execute("INSERT INTO solventmixer (batch_number, solvent_name, buffer_name, target_weight) "
                 "VALUES (%s, %s, %s, %s)",
                 (batch_number, solvent_name, selected_buffer[0], target_weight))
buffer_mix_db.commit()

# Print a message to confirm the insertion
print("{} added to the solventmixer table.".format(solvent_name))
"""


