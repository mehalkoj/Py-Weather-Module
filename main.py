import requests
import sqlite3
import os
from datetime import datetime, timedelta


path = rf"./weather.db"
conn = sqlite3.connect(rf'./weathermod.db')
c = conn.cursor()


# Class that handles the Weather api
# When an object is created with this class it should spill out a data paired with front end code
# So Class should be called, data formatted, then shown on front end correctly
class Weather:
    def __init__(self, apikey, key):
        self.apikey = apikey
        self.key = key

    def getweather(self, endpoint):

        if self.datacheck() == True:
            response = requests.get(endpoint + self.key + "?apikey=" + self.apikey)
            if response.status_code == 200:
                data = response.json()
                print("Recieving JSON")
                self.handledata(data)
            elif response.status_code != 200:
                return("Error Connecting To Weather Gods")
        elif self.datacheck() == False:
            # This is if it doesnt need to connect to api to get new data (ie. data that is younger than 5 hours)
            print("Data Up To Date!")
        # Should be calling a method that grabs the data that is in the table and sending it to the front end for display
        # This should happen regardless of the data check is true or false
        
       # self.displaydata()


        # Testing Purposes
        self.printdata()
        


    def handledata(self, data):
        for i in data:
                date_time = i['DateTime']
                weather_icon = i['WeatherIcon']
                has_precip = i['HasPrecipitation']
                temp = i['Temperature']['Value']
                precip_prob = i["PrecipitationProbability"]
                formatted = self.dateformat(date_time)
                x = self.dbinsert(formatted, weather_icon, has_precip, temp, precip_prob)

                


    def printdata(self):
        a = c.execute('''SELECT * FROM HOURWEATHER''').fetchall()
        for x in a:
            print(x)
    

    def dateformat(self, date_time):
        date = datetime.fromisoformat(date_time)
        #original_timezone_offset = timedelta(hours=8)  # Assuming +08:00
        #mountain_timezone_offset = timedelta(hours=-7)  # or -6 during daylight saving time
        #mountain_date = datetime.fromisoformat(date_time) - (timedelta(hours=8) - timedelta(hours=-7))
        formatted_date = date.strftime("%Y-%m-%d %H:%M")
        return formatted_date
    

    def killweather(self):
        c.execute('''DELETE FROM HOURWEATHER''')
        conn.commit()

    

    def dbinsert(self, date_time, weather_icon, has_precip, temp, precip_prob):
        # looping through API Data and inserting into table
        try:
            c.execute("INSERT INTO HOURWEATHER VALUES (?, ?, ?, ?, ?)", (date_time, weather_icon, has_precip, temp, precip_prob))
            conn.commit()

        except Exception as e:
            
            return print("ERROR: Something Went Wrong -", e)


    # Checks entry in db, compares time, if earliest entry is 5 hours before the current user time, pull data.
    def datacheck(self):
    
        c.execute('''SELECT Date FROM HOURWEATHER LIMIT 1''')
        out = c.fetchone()
        if out is None:
            return True
        else:
            user_time = datetime.now()
            data_timestamp = datetime.strptime(out[0], "%Y-%m-%d %H:%M")
            #time_dif = user_time - data_timestamp
            five = timedelta(hours=5)
            if (user_time - data_timestamp) >= five:
                self.killweather()
                return True
            else:
                return False



def createdb():

        hourweathertable = """ CREATE TABLE HOURWEATHER (
                    Date VARCHAR(255) NOT NULL,
                    Icon INT,
                    HasPrecip VARCHAR(255),
                    PrecipProb INT,
                    Temp REAL
                        )"""

        c.execute(hourweathertable)

        dailyweathertable = """CREATE TABLE DAILYWEATHER (
                    Date VARCHAR(255) NOT NULL,
                    TimeSet VARCHAR(255) NOT NULL,
                    Icon INT,
                    IconPhrase VARCHAR(255),
                    Precipitation VARCHAR(255),
                    MinTemp REAL,
                    MaxTemp REAL
                        )"""
        
        c.execute(dailyweathertable)

        conn.commit()
        





def initialize():
  
    a = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HOURWEATHER'")
    b = c.fetchone()

    if b == None:
        createdb()
        print("Database and Tables Created!")
    elif b == "HOURWEATHER":
        print("Files and Tables Exist, No Need For Setup")


def main():

    initialize()
    endpoint = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"
    apikey = input("Input API Key From Accuweather")
    key = input("Input location key from Accuweather")
    a = Weather(apikey, key)
    a.getweather(endpoint)


main()