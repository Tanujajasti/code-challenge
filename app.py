import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import pandas as pd


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

WEATHER_DATA_TABLE = "weather_data"
WEATHER_STATS_TABLE = "weather_stats"


def connect_to_db():
    conn = sqlite3.connect("main.db")
    return conn


def get_weather_data(st_id, record_dt, offset, page_size):
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    offset = (offset - 1) * page_size

    select_qry = f"SELECT * FROM {WEATHER_DATA_TABLE} "
    order_stmt = (
        f" ORDER BY weather_station, record_date LIMIT {page_size} offset {offset};"
    )

    condition = ""

    # When both STATION_ID and DATE passed
    if st_id and record_dt:
        condition = f"WHERE weather_station='{st_id}' AND record_date={record_dt}"

    # When only STATION_ID passed
    elif st_id:
        condition = f"WHERE weather_station='{st_id}'"

    # When only DATE passed
    elif record_dt:
        condition = f"WHERE record_date={record_dt}"

    cursor.execute(" ".join([select_qry, condition, order_stmt]))

    weather_data_records = cursor.fetchall()
    df = pd.DataFrame(
        weather_data_records,
        columns=[
            "rid",
            "weather_station",
            "record_date",
            "max_temp",
            "min_temp",
            "precipitation"
        ],
    )
    df.drop(['rid'], axis=1, inplace=True)
    return df.to_json(orient="records")


def get_weather_stats_data(st_id, record_year, offset, page_size):
    conn = connect_to_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    offset = (offset - 1) * page_size

    select_qry = f"SELECT * FROM {WEATHER_STATS_TABLE} "
    order_stmt = (
        f" ORDER BY weather_station, record_year LIMIT {page_size} offset {offset};"
    )

    condition = ""

    # When both STATION_ID and YEAR passed
    if st_id and record_year:
        condition = f"WHERE weather_station='{st_id}' AND record_year={record_year}"

    # When only STATION_ID passed
    elif st_id:
        condition = f"WHERE weather_station='{st_id}'"

    # When only YEAR passed
    elif record_year:
        condition = f"WHERE record_year={record_year}"

    cursor.execute(" ".join([select_qry, condition, order_stmt]))

    weather_data_records = cursor.fetchall()
    df = pd.DataFrame(
        weather_data_records,
        columns=[
            "rid",
            "record_year",
            "weather_station",
            "avg_max_temp",
            "avg_min_temp",
            "tot_precipitation"
        ],
    )
    df.drop(['rid'], axis=1, inplace=True)
    return df.to_json(orient="records")


@app.route("/api/weather", methods=["GET"])
def api_get_weather_data():
    args = request.args
    st_id = args.get("station_id", "", type=str)
    record_dt = args.get("date", "", type=str)
    offset = args.get("offset", 1, type=int)
    page_size = args.get("limit", 1000, type=int)
    records = get_weather_data(st_id, record_dt, offset, page_size)
    return {"data": json.loads(records)}


@app.route("/api/weather/stats", methods=["GET"])
def api_get_weather_stats():
    args = request.args
    st_id = args.get("station_id", "", type=str)
    record_year = args.get("year", "", type=str)
    offset = args.get("offset", 1, type=int)
    page_size = args.get("limit", 1000, type=int)
    records = get_weather_stats_data(st_id, record_year, offset, page_size)
    return {"data": json.loads(records)}


if __name__ == "__main__":
    app.debug = True
    app.run(debug=True)
    app.run()  # run app
