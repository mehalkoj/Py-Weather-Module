import sqlite3
import os

path = rf"./weather.db"
conn = sqlite3.connect(rf'./weathermod.db')
c = conn.cursor()

try:
    a = c.execute('''SELECT * FROM HOURWEATHER''').fetchall()
    for x in a:
        print(x)
        
    b = c.execute('''SELECT * FROM DAILYWEATHER''').fetchall()
    for s in b:
        print(s)

except Exception as e:
    print("Something Went Wrong -", e)