import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """These are the available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

# create the flask route for precipitation
# similar to the prcp hw activity
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    """These are the prcp value."""
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_date).\
    order_by(Measurement.date).all()

    # prcp for date will pull in the prcp data for each date
    prcp_dic = {date: prcp for date, prcp in results}

    return jsonify(prcp_dic)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of all stations within dataset."""
    # Query all passengers
    stations_results = session.query(Station.station, Station.name).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(stations_results))
        
    return jsonify(all_stations)
        
@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)
    """These are the temperature values."""
    one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # similar to prcp link
    date_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year_date).\
    order_by(Measurement.date).all()

    # temperature for date will pull in the temperature data for each date
    prcp_temp = {date: tobs for date, tobs in date_results}

    return jsonify(prcp_temp)

    # create a start and end link
    # use date from start of vacation to end vacation
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start=None, end=None):
    session = Session(engine)

    # if user only puts in one date, will use start_results
    if not end:
        start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
        return jsonify(start_results)

    # if user puts in two dates
    end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify(end_results)

if __name__ == "__main__":
    app.run(debug=True)


    

