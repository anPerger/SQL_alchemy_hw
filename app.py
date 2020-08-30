import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import pandas as pd

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>tobs</a><br/>"
        f"<a href='/api/v1.0/start date to end date'>start_to_end</a>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    # Query all passengers
    measurement_results = session.query(Measurements.station, Measurements.date,
        Measurements.prcp, Measurements.tobs).all()

     
    
    measurement_dates = []
    measurement_prcps = []
   
    for result in measurement_results:
        
        measurement_date = result[1]
        measurement_prcp = result[2]

        measurement_dates.append(measurement_date)
        measurement_prcps.append(measurement_prcp)

        # date_prcp[measurement_date] = measurement_date
        # date_prcp[prcp] = prcp

    prcp_dict = {}
    for date in range(len(measurement_dates)):
        prcp_dict[measurement_dates[date]] = measurement_prcps[date]
        
    
    
    session.close()
    print(prcp_dict)
    # Convert list of tuples into normal list
    date_prcps = list(np.ravel(prcp_dict))

    return jsonify(date_prcps)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    
    station_results = session.query(Stations.station, Stations.latitude, Stations.longitude, 
        Stations.elevation).all()

    
    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    measurement_results = session.query(Measurements.station, Measurements.date,
        Measurements.prcp, Measurements.tobs).all()
  
    measurement_dates = []
    measurement_tobs = []
    measurement_stations = []
    
    for result in measurement_results:
        
        measurement_date = result[1]
        measurement_tob = result[3]
        measurement_station = result[0]

        measurement_dates.append(measurement_date)
        measurement_tobs.append(measurement_tob)
        measurement_stations.append(measurement_station)
    
     tobs_dict = {}
    for date in range(len(measurement_dates)):
        tobs_dict[measurement_dates[date]] = measurement_tobs[date]
    
    print(tobs_dict)

    return jsonify(tobs_dict)

@app.route("/api/v1.0/start_to_end")
def start_to_end():

    session = Session(engine)

    




if __name__ == '__main__':
    app.run(debug=True)