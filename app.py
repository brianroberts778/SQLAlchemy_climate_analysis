import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#####################################################
# Database Setup
#####################################################
engine = create_engine("sqlite:////Users/brianroberts1/Documents/GitHub/SQLAlchemy_climate_analysis/Resources_hawaii.sqlite")

# Reflect and existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save the reference to the table
measurements = Base.classes.measurement
stations = Base.classes.station

#####################################################
# Flask Setup
#####################################################
app = Flask(__name__)


#####################################################
# Flask Routes
#####################################################
@app.route("/")
def Home():

    """List all routes that are available."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0.precipitation<br/>"
        f"/api/v1.0.stations<br/>"
        f"/api/v1.0.tobs<br/>"
        f"/api/v1.0.start<br/>"
        f"/api/v1.0.start/end<br/>"
    )


@app.route("/api/v1.0.precipitation")
def precipitation():

    # Create the session (link) from Python to the DB
    session = Session(engine)

    """Return dates and prcp values for all stations"""
    # Query for the dates and prcp values
    results = session.query(measurements.date, measurements.prcp).\
                     order_by(measurements.date).all()

    # Create list to hold results
    dates_prcps = []

    # Save the data as a dictionary, with date as the key and prcp as the values
    for date, prcp in results:
         prcp_dict = {}
         prcp_dict[date] = prcp
         dates_prcp.append(prcp_dict)

    session.close()

    # Return the json representation of the dictionary
    return jsonify(dates_prcp)

@app.route("/api/v1.0.stations")
def stations():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    """Return indentifying data for all stations"""
    # Query the stations
    results = session.query(stations.station, stations.name).all()
    
    # Create dict for query results
    station_dict = {}
    
    for station, name in results:
        station_dict[station] = name

    session.close()

    # Return the json representation of the dictionary
    return jsonify(station_dict)

@app.route("/api/v1.0.tobs")
def tobs():
    # Create the session (link) from Python to the DB
    session = Session(engine)

    """Return date and temp data of the most active station over the last year recorded"""

    # The last date and last year date were found in Jupyter Notebook
    last_date = '2017-08-23'
    last_year_date = '2016-08-23'

    # Query for date and temp data for the most active station, between our two dates
    # Most active station was determined in Jupyter Notebook
    results = session.query(measurements.date, measurements.tobs).\
              filter(measurements.date >= last_year_date).\
              filter(measurements.station == 'USC00519281').\
              order_by(measurements.date).all()

    # Create a list to hold results
    tobs_list = []

    # Save the data as a dictionary, with date as the key and tobs as the values
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    session.close()

    return jsonify(tobs_list)


# Return a JSON list of the minimum temperature, the average temperature,...
# ..and the max temperature for a given start or start-end range.

@app.route("/api/v1.0/<start>")
def temps_start(start_date):

    # Create the session (link) from Python to the DB
    session = Session(engine)

    """ When given the start only, calculate TMIN, TAVG, and TMAX 
    for all dates greater than and equal to the start date.
    start_date (string): %Y-%m-%d """

    # Query the database for required statistics
    results = session.query(measurements.date,\
              func.min(measurements.tobs), \
              func.avg(measurements.tobs), \
              func.max(measurements.tobs)).\
              filter(measurements.date >= start_date).\
              group_by(measurements.date).all()

    # Create a list to hold results
    start_list = []

    # Append results into a dictionary to be jsonified
    for date, min, max in results:
        start_dict = {}
        start_dict["Date"] = date
        start_dict["TMIN"] = min 
        start_dict["TAVG"] = avg 
        start_dict["TMAX"] = max 
        start_list.append(start_dict)

    session.close()

    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def temps_start(start_date, end_date):

    # Create the session (link) from Python to the DB
    session = Session(engine)

    """ When given the start and end dates, calculate TMIN, TAVG, and TMAX 
    for the given date range.
    start_date, end_date (string): %Y-%m-%d """

    # Query the database for required statistics
    results = session.query(measurements.date,\
              func.min(measurements.tobs), \
              func.avg(measurements.tobs), \
              func.max(measurements.tobs)).\
              filter(measurements.date >= start_date, measurements.date <= end_date).\
              group_by(measurements.date).all()

    # Create a list to hold results
    start_end_list = []

    # Append results into a dictionary to be jsonified
    for date, min, max in results:
        start_end_dict = {}
        start_end_dict["Date"] = date
        start_end_dict["TMIN"] = min 
        start_end_dict["TAVG"] = avg 
        start_end_dict["TMAX"] = max 
        start_end_list.append(start_end_dict)

    session.close()

    return jsonify(start_end_list)

if __name__ == '__main__':
    app.run(debug=True)






     