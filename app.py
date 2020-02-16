import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify, request
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return (
        f"Check out the Hawaii Climate API!<br/>"
        f"<br/>"
        f"Here are all of the available routes:<br/>"
        f"<br/>"
        f"Precipitation Analysis:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Stations:<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observations (for the previous year):<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"List of Min, Avg, & Max Temperature for a Start Date:<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"<br/>"
        f"List of Min, Avg, & Max Temperature for a Start--End Range:<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_data_point = (
        session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    )

    last_year = dt.datetime.strptime(last_data_point, "%Y-%m-%d") - dt.timedelta(
        days=365
    )

    prcp_last_year = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= last_year)
        .order_by(Measurement.date)
        .all()
    )

    prcp_last_year_dict = dict(prcp_last_year)

    return jsonify(prcp_last_year_dict)


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    last_data_point = (
        session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    )

    last_year = dt.datetime.strptime(last_data_point, "%Y-%m-%d") - dt.timedelta(
        days=365
    )

    prcp_last_year = (
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date >= last_year)
        .order_by(Measurement.date)
        .all()
    )

    prcp_last_year_dict = dict(prcp_last_year)

    return jsonify(prcp_last_year_dict)


@app.route("/api/v1.0/<start>")
def start_date(start):
    temp_list = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .all()
    )

    temp_list_dict = dict(
        Min_Temperature=temp_list[0][0],
        Avg_Temperature=temp_list[0][1],
        Max_Temperature=temp_list[0][2],
    )

    return jsonify(temp_list_dict)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    temp_list = (
        session.query(
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs),
            func.max(Measurement.tobs),
        )
        .filter(Measurement.date >= start)
        .filter(Measurement.date <= end)
        .all()
    )
    temp_list_dict = dict(
        Min_Temperature=temp_list[0][0],
        Avg_Temperature=temp_list[0][1],
        Max_Temperature=temp_list[0][2],
    )

    return jsonify(temp_list_dict)


if __name__ == "__main__":
    app.run(debug=True)
