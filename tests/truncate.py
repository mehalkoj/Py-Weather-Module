import os
import sqlite3

conn = sqlite3.connect(rf'../weathermod.db')
c = conn.cursor()

def removetable():
    try:
        c.execute("DROP TABLE HOURWEATHER")
        conn.commit()
        print("Table Removed!")
        
    
    except Exception as e:
        print("Issue Dropping Weather Table", e)


def removedata():
    try:
        c.execute("DELETE FROM HOURWEATHER")
        conn.commit()
        print("Data Removed!")


    except Exception as e:
        print("Issue dropping data from the HOURWEATHER table", e)
 

"""def removedb():
    file = "weathermod.db"
    try:
        os.remove("../weathermod.db")
        print("DB File Removed!")

    except Exception as e:
        print("Issue Removing DB File", e)
"""

def main():
    print("1. Remove Table")
    print("2. Remove Data From Table")
    #print("3. Remove Database")

    select = input("Select Which Action You Want! ")

    match select:
        case "1":
            removetable()
        case "2":
            removedata()
        #case "3":
            #removedb()

main()
conn.close()        