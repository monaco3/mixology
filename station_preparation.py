"""
Here we prepare the chemicals that need to be used and assign them to a specific pump.
"""


import mysql.connector

# establishing the connection to the database
buffer_mix_db = mysql.connector.connect(
  host="localhost", #"localhost",
  user="phdd",  #"yourusername",
  password="root",  # "yourpassword",
  database="BufferStationDB", #"yourdatabase"
)

#Creating a cursor object using the cursor() method
mycursor = buffer_mix_db.cursor()
"""
# mycursor.execute("CREATE DATABASE BufferStationDB")

#Create Chemical Composition table if it does not already exist
mycursor.execute("CREATE TABLE chemicals(chemID int PRIMARY KEY AUTO_INCREMENT, "
                 "chemName VARCHAR (255) NOT NULL,"
                 "availAmount float UNSIGNED ,"
                 "stamp_created timestamp default now(),"
                 "stamp_updated timestamp default now() on update now(),"
                 "addedAmount float UNSIGNED, molarWeight float UNSIGNED,"
                 "pumpNo int UNSIGNED)")
buffer_mix_db.commit()
"""


"""
#Delete the unwanted table

#Prompt the user to enter the name of the table to delete
tableName = input("Enter the name of the table to delete: ")
mycursor.execute("DROP TABLE {}".format(tableName))
# Print a message to confirm the deletion
print("{} table deleted.".format(tableName))

#End table deletion
"""
#Retrieving the list of tables print("List of tables in the database: ")
#mycursor.execute("SHOW Tables")
#print(mycursor.fetchall())
"""
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
"""
"""
# Execute a SELECT statement to fetch all rows from the chemicals table
mycursor.execute("SELECT * FROM bufferstationdb.chemicals")
# Fetch all rows and print them
rows = mycursor.fetchall()
for row in rows:
    print(row)
"""



"""
#Creating a buffer table. Each buffer can have different number of chemicals
mycursor.execute("CREATE TABLE buffers(buffer_id  int PRIMARY KEY AUTO_INCREMENT, "
                 "buffer_name VARCHAR (255) NOT NULL,"
                 "buffer_weight FLOAT NOT NULL,"
                 "buffer_created timestamp default now(),"
                 "buffer_updated timestamp default now() on update now(),"
                 "chemical_1 VARCHAR(255) NOT NULL,"
                 "chemical_1_weight FLOAT NOT NULL,"
                 "chemical_2 VARCHAR(255),"
                 "chemical_2_weight FLOAT,"
                 "chemical_3 VARCHAR(255),"
                 "chemical_3_weight FLOAT,"
                 "chemical_4 VARCHAR(255),"
                 "chemical_4_weight FLOAT,"
                 "chemical_5 VARCHAR(255),"
                 "chemical_5_weight FLOAT,"
                 "chemical_6 VARCHAR(255),"
                 "chemical_6_weight FLOAT,"
                 "chemical_7 VARCHAR(255),"
                 "chemical_7_weight FLOAT,"
                 "chemical_8 VARCHAR(255),"
                 "chemical_8_weight FLOAT,"
                 "chemical_9 VARCHAR(255),"
                 "chemical_9_weight FLOAT,"
                 "chemical_10 VARCHAR(255),"
                 "chemical_10_weight FLOAT,"
                 "chemical_11 VARCHAR(255),"
                 "chemical_11_weight FLOAT,"
                 "chemical_12 VARCHAR(255),"
                 "chemical_12_weight FLOAT )")
buffer_mix_db.commit()
"""

"""
# Retrieve the list of available chemicals from the database
mycursor.execute("SELECT chemName FROM chemicals")
chemical_list = mycursor.fetchall()

# Prompt the user to select a chemical from the list
print("Select a chemical from the list below:")  #Maybe the selection should start with the most important for the buffer
for i, chemical in enumerate(chemical_list):
    print("{}. {}".format(i+1, chemical[0]))
"""

"""
# Get a list of all chemicals from the chemicals table
mycursor.execute("SELECT chemName FROM chemicals")
chemicals_list = [x[0] for x in mycursor.fetchall()]

# Initialize the buffer dictionary
buffer_dict = {}

# Prompt the user to select chemicals from the list and add them to the buffer
while True:
  # Display the list of chemicals to the user
  print("Chemicals list:")
  for i, chem in enumerate(chemicals_list):
    print(f"{i + 1}. {chem}")

  # Prompt the user to select a chemical and enter its weight
  chem_choice = int(input("Enter the number of the chemical you want to add to the buffer: "))
  chem_name = chemicals_list[chem_choice - 1]
  chem_weight = float(input("Enter the weight of the chemical in grams: "))

  # Add the chemical and its weight to the buffer dictionary
  buffer_dict[chem_name] = chem_weight

  # Ask the user if they want to add more chemicals to the buffer
  choice = input("Do you want to add another chemical to the buffer? (YES/NO): ")
  if choice.lower() != "yes":
    break

# Insert the buffer into the buffer table
buffer_name = input("Enter a name for the buffer: ")
buffer_weight = sum(buffer_dict.values())
buffer_values = [buffer_name, buffer_weight]
for chem_name, chem_weight in buffer_dict.items():
  buffer_values.append(chem_name)
  buffer_values.append(chem_weight)

# Insert the buffer values into the buffer table
buffer_query = "INSERT INTO buffers (buffer_name, buffer_weight"
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

print("Buffer added to the buffer table.")

"""


"""
# create the solventmixer table
mycursor.execute("CREATE TABLE solventmixer ("
                 "solvent_id INT PRIMARY KEY AUTO_INCREMENT,"
                 "batch_number VARCHAR(255) NOT NULL,"
                 "solvent_name VARCHAR(255),"
                 "buffer_name VARCHAR(255),"
                 "target_weight FLOAT,"
                 "actual_weight FLOAT,"
                 "solv_creation_date TIMESTAMP DEFAULT NOW()"
                 ")")

# commit the changes to the database
buffer_mix_db.commit()

# close the database connection
buffer_mix_db.close()
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


# # Select 10 liquids from the database by their names
# liquids = []
# liquid_names = ['water', 'glycerol', 'ethanol', 'coffee', 'tea', 'milk', 'soup', 'porridge', 'cola', 'juice']
# for name in liquid_names:
#     cursor.execute("SELECT proportion FROM liquids WHERE name = %s", (name,))
#     proportion = cursor.fetchone()
#     if proportion:
#         liquids.append((name, proportion[0]))
#
# # Assign each liquid to a pump
# pumps = []
# for i in range(10):
#     pumps.append(input("Assign pump for {} (Pump 1-10): ".format(liquids[i][0])))
#
# # Print the assigned pumps for each liquid
# print("Liquid assignments:")
# for i in range(10):
#     print("{}: Pump {}".format(liquids[i][0], pumps[i]))
#
# # Close the database connection
# buffer_mix_db.close()
