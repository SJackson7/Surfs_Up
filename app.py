# dependencies
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify, request

#######################################################
# database setup
#######################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite', connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# create session from Python to the db
session = Session(engine)

#######################################################
# database setup
#######################################################
app_climate = Flask(__name__)

@app_climate.route('/')
def welcome():
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/><br/>'
        f'<b>For "temp" route, enter the start date followed by "/" and end date<br/>'
        f'Date format must be "YYYY-MM-DD"<br/></b>'
        f'/api/v1.0/temp/<br/>'
    )

@app_climate.route('/api/v1.0/precipitation')
# returns JSONified precipitation data for the last year in the database
def precipitation():
    # calculate the date one year from the last date in data set (today equals 8/23/2017).
    today = dt.datetime(2017,8,23)
    prev_year = (today) - dt.timedelta(days=365)

    # perform a query to retrieve the data and precipitation scores
    results = session.query(measurement.date, measurement.prcp)\
                .filter(measurement.date >= prev_year)\
                .order_by(measurement.date).all()

    # create a dictionary from the row data and append to a list of all_precip
    all_precip = []
    for precipitation in results:
        precip_dict = {}
        precip_dict[precipitation.date] = precipitation.prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app_climate.route('/api/v1.0/stations')
# returns JSONified data of all the stations in the database
def statiions():
    # query all stations
    station_results = session.query(station.name).all()

    # convert list of tuples into normal list
    all_stations = list(np.ravel(station_results))

    return jsonify(all_stations)

@app_climate.route('/api/v1.0/tobs')
# return JSONified data for the most active station for the last year of data
def tobs():
    # query to find the most active stations
    # list the stations and the counts in descending order.
    active_stations = session.query(measurement.station, func.count(measurement.station))\
                            .group_by(measurement.station)\
                            .order_by(func.count(measurement.station).desc()).all()

    # get most active station and set to variable, index 0,0 as previous result sorted high to low
    most_active_station = active_stations[0][0]
    print(most_active_station)

    # calculate the date one year from the last date in data set (today equals 8/23/2017).
    today = dt.datetime(2017,8,23)
    prev_year = (today) - dt.timedelta(days=365)

    # return JSON list of all temperature observations one-year from last date in dataset
    tobs_results = session.query(measurement.tobs)\
                    .filter(measurement.date >= prev_year)\
                    .filter(measurement.station == most_active_station)\
                    .order_by(measurement.date).all()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(tobs_results))

    return jsonify(all_tobs)

@app_climate.route("/api/v1.0/temp/<start>")
@app_climate.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
   """Return TMIN, TAVG, TMAX."""
   # select statement for min, avg and max functions
   sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]

   # addding 'if-not' statement to determine start/end dates
   if not end:
       # calculate TMIN, TAVG, TMAX for dates greater than start
       results = session.query(*sel).\
           filter(measurement.date >= start).all()

       # Unravel results into a 1D array and convert to a list
       temps = list(np.ravel(results))
       return jsonify(temps)

   # calculate TMIN, TAVG, TMAX with start and stop
   results = session.query(*sel).\
       filter(measurement.date >= start).\
       filter(measurement.date <= end).all()

   # unravel results into a 1D array and convert to a list
   temps = list(np.ravel(results))
   return jsonify(temps=temps)

if __name__ == '__main__':
    app_climate.run(debug=True)
