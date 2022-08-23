## Surf's Up!

For this exercise, I analyzed and explored the climate data for Honolulu, Hawaii. The exercise was split into three parts. 

#### Part 1: Analyze and Explore the Climate Data
The climate Jupyter Notebook file contains a basic climate analysis and data exploration of the climate database. Using SQLAlchemy ORM queries, Pandas, and Matplotlib, I was able to analyze both precipitation and weather station data to determine the best time and location to visit. The climate data contained information through 8/23/2017; I examined a one-year period. 


#### Daily Precipitation Analysis
After connecting to the SQLite database file and reflecting the tables into classes, I was able to create the following chart showing daily precipitation amounts from 8/23/2016 through 8/23/2017 (full-size image is available in the Image folder):

![image](https://user-images.githubusercontent.com/104914008/186263215-d90057a1-6479-4317-bd94-e41af7a5df3b.png)

Here are the summary statistics for the daily precipitation. Note that the average rainfall during the one-year period was near 0.2". 
![image](https://user-images.githubusercontent.com/104914008/186263672-f7993cc0-0df2-4b33-83a6-f29638f5aac1.png)

#### Station Analysis
The next item I examined was the weather stations, particularly the weather station that had the most data (rows) in the SQL database. This allowed me to see the observed temperatures (TOBS) for the one-year period. I identified weather station USC00519281 as the most active and therefore used its data for this part of the exercise. Once I obtained and filtered the desired information, I created a histogram to see what temperature occurs most frequently; most of the time it was around 75°F (full-size image is available in the Image folder):
![image](https://user-images.githubusercontent.com/104914008/186264701-181d6b7f-4b7e-4c12-9285-e5032c57d0ba.png)


### Part 2: Design a Climate App
Now that I completed my initial analysis, I designed a Flask API based on the queries developed for this exercise. The API has the following routes.
* /api/v1.0/precipitation
  * converts the precipitation query results to a dictionary and then returns a JSON representation
* /api/v1.0/stations
  * returns a JSON list of the stations from the dataset
* /api/v1.0/tobs
  * queries the dates and temperature observations of the most-active station for the previous year of data
  * returns aJSON list of temperature observations for the previous year
* /api/v1.0/temp/
  * returns a JSON list of the minimum, average, and maximum temperatures for a specified start or start-end range of dates
  * route allows entry of start data and end date and must be in yyyy-mm-dd format (noted on API route page)
 
#### Temperature Analysis: June versus December
For an extra look and knowing that Hawaii has the reputation of enjoying mild weather all year round, I checked to see if there is any meaningful difference in the temperatures between June and December. For this bonus, I looked at all dates and years where the month was either June or December. 

First, I identified the average temperatures across all stations for June and December. I then completed a t-test and box and whisker diagram (full-size image is available in the Image folder) to see any statistical significance. Using an unpaired t-test since the two datasets are independent from one-another, the probability value was very near zero and therefore indicated there is not an meaningful difference in temperatures. Either June or December would be a good time to visit, though December has a better chance of being cooler, but a further look is needed into precipitation before booking your vacation. 

![image](https://user-images.githubusercontent.com/104914008/186266455-d02f3fe1-76ee-4d0e-9de3-9525f7011a4a.png)

