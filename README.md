# Py Weather Module
The purpose of this is to have a standalone module that works with another project. This is used to grab the AccuWeather API data. You can input a key for the location and the API key for the data.
At the moment it is only 12 Hour data and for the project that this is apart of and the limits of a free weather API I have it pull new data only when the data stored is 5 hours old.


## Things To Do
Currently I completed my main goal with this module. Have data from the weather API pulled in for the 12 Hour forecast and the 5 day forecast. To get around the limitations of the free api (call limit).
I implemented a way for it to only call the API data if the date / time of the current user is 5 hours ahead or a day ahead of the oldest piece of data. What is left is to do any clean up of the code including organization and bugs.


## What About The Other Tool
The tool that this will be apart of is a multi tool for desktop that will be pulling in stock data, news data, and other cool little features.
