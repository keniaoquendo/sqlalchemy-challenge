# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Starter_code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station= Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"--Preciptation Totals for 2016-2017: <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<br/>"
        f"--Active Weather stations: <a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"--Daily Temperature Observations for Station USC00519281 for 2016-2017: <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f"--Min, Average & Max Temperatures for Date Range: <a href=\"/api/v1.0/<start\"<br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query precipitation across all stations
    sel =[measurement.date, func.sum(measurement.prcp)]
    precipitation = session.query(*sel).\
        filter(measurement.date >= '2016-08-23').\
        group_by(measurement.date).\
        order_by(measurement.date).all()

    session.close()

precipitation_dates=[]
precipitation_totals= []
   
for date, dailytotal in precipitation:
        precipitation_dates.append(date)
        precipitation_totals.append(dailytotal)

precipitation_dict= dict(zip(precipitation_dates, precipitation_totals))


return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    


@app.route("/api/v1.0/tobs")
def temperatures():
    session= Session(engine)
    
    session.close()

   

if __name__ == '__main__':
    app.run(debug=True)