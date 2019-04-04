import numpy as np 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///../Resoures/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
app = Flask(__name__)

@app.route("/")
def homepage():
    """List all routes that are available."""
    return (
        f"List all routes that are available:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"List of precipitation from last year from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"List of stations from the dataset<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"List of Temperature Observations (tobs) for the previous year<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"List of the minimum temperature, the average temperature, and the max temperature for a given start<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"List of the minimum temperature, the average temperature, and the max temperature for a given start-end range<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """List of precipitation from last year from all stations:"""
    latest_data = session.query(Measurement.date).order_by(Measurement.date.desc()).first() 
    latest_data = latest_data [0]
    first_date = dt.datetime.strptime(latest_data,"%Y-%m-%d") - dt.timedelta(days=366)
    lastyear = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date >= first_date).order_by(Measurement.date).all()
    precipitation_list = dict(lastyear)
    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():
    """List of stations from the dataset:"""
    active_station = session.\
    query(Measurement.station).\
    group_by (Measurement.station).all()
    stations_list= list(np.ravel( active_station))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """List of Temperature Observations (tobs) for the previous year:"""
    atest_data = session.query(Measurement.date).order_by(Measurement.date.desc()).first() 
    latest_data = latest_data [0]
    first_date = dt.datetime.strptime(latest_data,"%Y-%m-%d") - dt.timedelta(days=366)
    result_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= first_date).all()
    tobs_list = list(result_tobs )
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def daily_normals(start):
    """List of the minimum temperature, the average temperature, and the max temperature for a given start:"""
    start_trip = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    start_list=list(start_trip)
    return jsonify(start_list)

@app.route("/api/v1.0/<start>/<end>")
def daily_trips(start,end):
    """List of the minimum temperature, the average temperature, and the max temperature for a given start-end range:"""
    trips_dates = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    trips_dates_list=list(trips_dates)
    return jsonify(trips_dates_list)

if __name__ == "__main__":
    app.run(debug=True)

