import requests
import sqlite3
import os
from datetime import *


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

    def getweather(self):

        hourlyendpoint = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"
        dailyendpoint = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"

        if self.hourlydatacheck() == True:
            response = requests.get(hourlyendpoint + self.key + "?apikey=" + self.apikey)
            if response.status_code == 200:
                data = response.json()
                print("Recieving JSON")
                self.handlehourdata(hourlyendpoint, data)
            elif response.status_code != 200:
                return("Error Connecting To Weather Gods")
        elif self.hourlydatacheck() == False:
            # This is if it doesnt need to connect to api to get new data (ie. data that is younger than 5 hours)
            print("Data Up To Date!")
        
        if self.dailydatacheck() == True:
            response = requests.get(dailyendpoint + self.key + "?apikey=" + self.apikey)
            if response.status_code == 200:
                data = response.json()
                print("Recieving JSON")
                self.handledailydata(dailyendpoint, data)
            elif response.status_code != 200:
                return("Error Connecting To Weather Gods")
        elif self.dailydatacheck() == False:
            # This is if it doesnt need to connect to api to get new data (ie. data that is younger than 5 hours)
            print("Data Up To Date!")


        self.printdata()
        




        # Should be calling a method that grabs the data that is in the table and sending it to the front end for display
        # This should happen regardless of the data check is true or false
        
       # self.displaydata()


        # Testing Purposes
        
        
    def handlehourdata(self, hourlyendpoint, data):
        try:
            for i in data:
                        date_time = i['DateTime']
                        weather_icon = i['WeatherIcon']
                        has_precip = i['HasPrecipitation']
                        temp = i['Temperature']['Value']
                        precip_prob = i["PrecipitationProbability"]
                        formatted = self.dateformat(date_time)
                        x = self.dbinserthourly(formatted, weather_icon, has_precip, temp, precip_prob)
        except Exception as e:
            return print("Something Went Wrong - ", e)


# Loops daily data and inserts it into db
    def handledailydata(self, dailyendpoint, data):
        try:
            x = self.dbinsertdaily
            for i in data['DailyForecasts']:
                date = i['Date']
                mintemp = i['Temperature']['Minimum']['Value']
                maxtemp = i['Temperature']['Maximum']['Value']
                dayicon = i['Day']['Icon']
                nighticon = i['Night']['Icon']
                dayprecip = i['Day']['HasPrecipitation']
                nightprecip = i['Night']['HasPrecipitation']
        
                # Checks if certain values exist so it does not give error
                daypreciptype = dayprecipinten = nightpreciptype = nightprecipinten = None

                if dayprecip:
                    daypreciptype = i['Day'].get('PrecipitationType')
                    dayprecipinten = i['Day'].get('PrecipitationIntensity')

                if nightprecip:
                    nightpreciptype = i['Night'].get('PrecipitationType')
                    nightprecipinten = i['Night'].get('PrecipitationIntensity')

                x(date, mintemp, maxtemp, dayicon, nighticon, dayprecip, daypreciptype, dayprecipinten, nightprecip, nightpreciptype, nightprecipinten)

        except Exception as e:
            print("Error in handledailydata:", e)


                
                


    def printdata(self):
        try:
            a = c.execute('''SELECT * FROM HOURWEATHER''').fetchall()
            for x in a:
                print(x)
        
            b = c.execute('''SELECT * FROM DAILYWEATHER''').fetchall()
            for s in b:
                print(s)
        except Exception as e:
            print("Something Went Wrong -", e)
    

    def dateformat(self, date_time):
        date = datetime.fromisoformat(date_time)
        #original_timezone_offset = timedelta(hours=8)  # Assuming +08:00
        #mountain_timezone_offset = timedelta(hours=-7)  # or -6 during daylight saving time
        #mountain_date = datetime.fromisoformat(date_time) - (timedelta(hours=8) - timedelta(hours=-7))
        formatted_date = date.strftime("%Y-%m-%d %H:%M")
        return formatted_date
    
    

    def dbinserthourly(self, date_time, weather_icon, has_precip, temp, precip_prob):
        # looping through API Data and inserting into table
        try:
            c.execute("INSERT INTO HOURWEATHER VALUES (?, ?, ?, ?, ?)", (date_time, weather_icon, has_precip, temp, precip_prob))
            conn.commit()

        except Exception as e:
            
            return print("ERROR: Something Went Wrong -", e)


    def dbinsertdaily(self, date, mintemp, maxtemp, dayicon, nighticon, dayprecip, nightprecip, daypreciptype=None, dayprecipinten=None,
                                nightpreciptype=None, nightprecipinten=None):
        # looping through API Data and inserting into table
        try:
            c.execute("INSERT INTO DAILYWEATHER VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (date, mintemp, maxtemp, dayicon, nighticon, dayprecip, nightprecip, daypreciptype, dayprecipinten,
                                nightpreciptype, nightprecipinten))
            conn.commit()

        except Exception as e:
            
            return print("ERROR: Something Went Wrong -", e)

    # Checks entry in db, compares time, if earliest entry is 5 hours before the current user time, pull data.
    def dailydatacheck(self):
            c.execute('''SELECT Date FROM DAILYWEATHER LIMIT 1''')
            out = c.fetchone()
            if out is None:
                return True
            else:
                user_date = date.today()
                stmp = out[0]
                date_stamp = datetime.strptime(stmp, '%Y-%m-%dT%H:%M:%S%z').date()
                if user_date > date_stamp:
                    print("Earliest Data Is Under Threshold")
                    c.execute('''DELETE FROM DAILYWEATHER''')
                    conn.commit()
                    return True
                else:
                    return False


    def hourlydatacheck(self):
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
                    c.execute('''DELETE FROM HOURWEATHER''')
                    conn.commit()
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
                    MinTemp REAL,
                    MaxTemp REAL,
                    DayIcon INT,
                    DayPrecipitation VARCHAR(255),
                    DayPrecipitationType VARCHAR(255),
                    DayPrecipitationIntensity VARCHAR(255),
                    NightIcon INT,
                    NightPrecipitation VARCHAR(255), 
                    NightPrecipitationType VARCHAR(255), 
                    NightPrecipitationIntensity VARCHAR(255)
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

    apikey = input("Input API Key ")
    key = input("Input City Key From AccuWeather ")
    a = Weather(apikey, key)
    a.getweather()


main()