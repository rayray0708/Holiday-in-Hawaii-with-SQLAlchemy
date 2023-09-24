import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import json

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#Start at the homepage.
# List all the available routes.
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        #Flask API will treat <start> and <end> as variables so they won't get displayed in the API route on the website
        # I have to and end start/ and end/ before these variables to display the correct routes
        "/api/v1.0/start/<start><br/>"
        "/api/v1.0/start/end/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Convert the query results to a dictionary by using date as the key and prcp as the value.
    #Return the JSON representation of your dictionary.
    precipitation_results = session.query(Measurement.date, Measurement.prcp).all()
    precipitation_results

    session.close()
    # Create a dictionary from the row data and append to a list of all_precipitations
    # all_precipitations = []
    precipitation_dict = {}
    for date, prcp in precipitation_results:
        precipitation_dict[date] = prcp

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Return a JSON list of stations from the dataset.
    stations_results = session.query(Station.station).all()
    session.close()

    #Create a list of dictionaries that hold the stations' names and return the output in json format
    all_stations = []
    for station in list(np.ravel(stations_results)):
        #print(station)
        station_dict = {
            'station':station
        }
        all_stations.append(station_dict)
        
    #all_stations = list(np.ravel(all_stations))
    return json.dumps(all_stations)

@app.route("/api/v1.0/tobs") #Don't have to include <br/> inside this URL because it's just a line breaker
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Calculate the date of year before the most recent date in the dataset
    one_year_before_date = dt.date(2017,8,23) - dt.timedelta(days=365)

    #Query to retrieve the dates and temperatures for the station USC00519281 in the past year
    temp_last_12_months = session.query(Measurement.date, Measurement.tobs).\
                                    filter(Measurement.date >= one_year_before_date).\
                                    filter_by(station = 'USC00519281').all()
    session.close()

    #Create a list of dictionaryies that holds the date and temp for each day in the past year,
    #return temperature_dict in json format
    temperature_list = []
    for date,tob in temp_last_12_months:
        print(f"{date},{tob}")
        temp_dict = {
            "date": date,
            "temperature": tob
        }
        temperature_list.append(temp_dict)
        #temperature_dict[date] = tob
    return json.dumps(temperature_list)


@app.route("/api/v1.0/start/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the start parameter from the URL to a datetime object
    #strptime() function stands for "string parse time." It is a method provided by the datetime module in Python
    # its allows you to parse a string representing a date and time and convert it into a datetime object.
    # It takes in 2 arguments: (1) string representing the date and time, (2) a format string that specifies how the date and time 
    # information is structured in the input string.
    # E.g., date_string = "2023-09-22 14:30:00"
    #       format_string = "%Y-%m-%d %H:%M:%S"
    # format_string specifies the format of the input string using format codes like %Y for the year, %m for the month, 
    # %d for the day, %H for the hour, %M for the minute, and %S for the second.
    start_date = dt.datetime.strptime(start, "%Y%m%d")

    # Query the database to get minimum, maximum, and average temperature data
    # results will return a list of 
    results = session.query(
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)
        ).filter(Measurement.date >= start_date).all() #Filter date column to retrieve dates at/later than start date

    session.close()

    # Unravel results into a dictionary
    temp_stats = {
        "Min Temperature": results[0][0],
        "Max Temperature": results[0][1],
        "Avg Temperature": round(float(results[0][2]),2)#convert and round result to 2 decimal places 
    }
    #the object 'results' will return something like this [(20, 15, 18)]
    #The square brackets [] indicate that the data is contained within a Python list. 
    # Lists are used to store ordered collections of items, and the square brackets are used to define and enclose the list.
    #The round brackets () are used to define a tuple. In this case, you have a single tuple within the list. 
    # A tuple is similar to a list in that it can store ordered elements, but unlike lists, tuples are immutable, 
    # which means their elements cannot be changed after creation.
    #You can access the elements within the list and tuple using indexing, e.g., my_list[0] to access the tuple 
    # and my_list[0][0] to access the first element within the tuple.
    
    return jsonify(temp_stats)

@app.route("/api/v1.0/start/end/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Convert start and end dates to datetime format
    start_date = dt.datetime.strptime(start, "%Y%m%d")
    end_date = dt.datetime.strptime(end, "%Y%m%d")

    #Return the min, max and avg for the temperatures withing the specified date range
    results = session.query(
    func.min(Measurement.tobs),
    func.max(Measurement.tobs),
    func.avg(Measurement.tobs)
    ).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    #print(type(results[0][2]))
    #Access the min, max and average in the results object 
    temp_stats = {
    "Min Temperature": results[0][0], #access the min temp from results
    "Max Temperature": results[0][1], #access the max temp from results
    "Avg Temperature": round(float(results[0][2]),2) #convert and round result to 2 decimal places 
    }

    #Display min, max and average in json format
    return jsonify(temp_stats)
    

if __name__ == '__main__':
    app.run(debug=True) #If debug is true, you don't have to re-run the script after a new change is added to the script, just ctrl+s 
    #and the URL links should work fine

