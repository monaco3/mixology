from private import *
# Creating a cursor object using the cursor() method
mycursor = buffer_mix_db.cursor()

#mycursor.execute("CREATE DATABASE IF NOT EXISTS BufferStationDB")

# Creating a table to store chemical details if it doesn't exist
mycursor.execute("CREATE TABLE IF NOT EXISTS chemicals ("
                 "chemID int PRIMARY KEY AUTO_INCREMENT, "
                 "chemName VARCHAR(255) NOT NULL, "
                 "availAmount float UNSIGNED, "
                 "stamp_created timestamp default now(), "
                 #"stamp_updated timestamp default now() on update now(), "
                 "addedAmount float UNSIGNED, "
                 "molarWeight float UNSIGNED, "
                 "pumpNo int UNSIGNED)")
buffer_mix_db.commit()


# #Delete the unwanted tables
# while True:
#     # Prompt the user to enter the name of the table to delete
#     tableName = input("Enter the name of the table to delete: ")
#     mycursor.execute("DROP TABLE IF EXISTS {}".format(tableName))
#     # Print a message to confirm the deletion
#     print("{} table deleted.".format(tableName))
#
#     # Ask if the user wants to delete another table
#     choice = input("Do you want to delete another table? (YES/NO)").lower()
#     if choice != "yes":
#         break
# #End table deletion


#Create a buffer table. Each buffer can have different number of chemicals
mycursor.execute("CREATE TABLE IF NOT EXISTS buffers(buffer_id  int PRIMARY KEY AUTO_INCREMENT, "
                 "buffer_name VARCHAR (255) NOT NULL,"
                 "buffer_weight FLOAT NOT NULL,"
                 "buffer_maker VARCHAR(255),"
                 "buffer_created timestamp default now(),"
                 #"buffer_updated timestamp default now() on update now(),"
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


#Create an intermediate  aka joining table to handle many to many relationsip connecting chemiacals and buffer tables
mycursor.execute("CREATE TABLE IF NOT EXISTS solventmix ("
                 "solvent_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
                 "buffer_id INT NOT NULL,"
                 "chem_id INT NOT NULL,"                 
                 "buffer_maker VARCHAR(255),"
                 "solvent_created timestamp default now(), "
                 #"PRIMARY KEY (buffer_id, chem_id),"
                 "FOREIGN KEY (buffer_id) REFERENCES buffers(buffer_id),"
                 "FOREIGN KEY (chem_id) REFERENCES chemicals(chemID)"
                 ")")
buffer_mix_db.commit()



#Create a table to store all the information of the final buffer making or solvent mixing.
#Here we add the batch_number, chamicals used, buffer_used, Target_chemical_weight, adjusted_chemical_weight, buffer_processor,
mycursor.execute("CREATE TABLE IF NOT EXISTS processedBuffer ("
                 "processedBuffer_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,"
                 "nameofbuffer_processor VARCHAR(255),"
                 "batch_number VARCHAR(255),"
                 "chem_id INT NOT NULL,"
                 "buffer_id INT NOT NULL,"
                 "original_weight FLOAT,"
                 "adjusted_weight FLOAT," 
                 "processed_time timestamp default now(),"                                                            
                 "FOREIGN KEY (buffer_id) REFERENCES buffers(buffer_id),"
                 "FOREIGN KEY (chem_id) REFERENCES chemicals(chemID)"
                 ")")
buffer_mix_db.commit()