import sqlite3


connection = sqlite3.connect("database", check_same_thread = True)
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Inventory_on (ID INT, 'Primary weapon' TEXT, 'Secondary weapon' TEXT, 'Melee attack' TEXT,"
               "Helmet TEXT, Armor TEXT, Gloves TEXT, Pants TEXT, Boots TEXT, 'Set' TEXT, Optional TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS Inventory_off (ID INT, '1' TEXT, '2' TEXT, '3' TEXT, '4' TEXT, '5' TEXT, '6' TEXT, '7' TEXT, '8' TEXT,"
               "'9' TEXT, '10' TEXT, '11' TEXT, '12' TEXT, '13' TEXT, '14' TEXT, '15' TEXT, '16' TEXT)")

cursor.execute("CREATE TABLE IF NOT EXISTS Players (ID INT, Clan TEXT, Nickname VARCHAR(20), Level INT,"
               "Attack INT, Defence INT, Experience INT, Money INT, Stamina INT, 'Stamina max' INT, Status TEXT, 'Battle money' INT, 'Battle exp' INT)")

cursor.execute("CREATE TABLE IF NOT EXISTS Clans (Name TEXT, Points INT)")

cursor.execute("CREATE TABLE IF NOT EXISTS WorkStatus (ID INT, Status INT, Status_2 INT)")

connection.commit()
connection.close()