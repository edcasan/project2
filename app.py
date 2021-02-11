from flask import Flask, render_template, jsonify
import pandas as pd
from sqlalchemy import create_engine
import os

app = Flask(__name__)

def get_data():
    connection_string=os.environ.get("DATABASE_URL", "")
    #connection_string = "postgres://postgres:12@localhost/vaccines"
    # with create_engine(connection_string) as conn:
    conn=create_engine(connection_string)
    data = pd.read_sql("select * from countries",conn)
    return data


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api_country")
def api_country():
    connection_string=os.environ.get("DATABASE_URL", "")
    #connection_string = "postgres://postgres:12@localhost/vaccines"
    conn = create_engine(connection_string)
    data = pd.read_sql("select * from countries",conn)

    country = data.groupby("country")["daily_vaccinations"].sum()

    return (
        country
        .reset_index()
        .loc[:,["country","daily_vaccinations"]]
        .sort_values(by="daily_vaccinations", ascending=False)
        .head(15)
        .to_json(orient="records")
    )

@app.route("/api_world")
def api_vaccines():
    connection_string=os.environ.get("DATABASE_URL", "")
    #connection_string = "postgres://postgres:12@localhost/vaccines"
    conn = create_engine(connection_string)
    data = pd.read_sql("select * from countries",conn)

    total_world = data.groupby("date")["daily_vaccinations"].sum()

    return (
        total_world
        .reset_index()
        .loc[:,["date","daily_vaccinations"]]
        .sort_values(by="date", ascending=False)
        .to_json(orient="records")
    )

@app.route("/api/country/<country>")
def api_daily(country):
    connection_string=os.environ.get("DATABASE_URL", "")
    #connection_string = "postgres://postgres:12@localhost/vaccines"
    conn = create_engine(connection_string)
    data = pd.read_sql("select * from countries",conn)
    dt = data.query(f'country == "{country}"')
    daily_country=dt[['country','date',"daily_vaccinations"]].groupby(['country']).agg(list)
    

    return(
        daily_country
        .to_json(orient="index")
    )

@app.route("/api/countries")
def countries():
    data = get_data()
    return jsonify(data.country.unique().tolist())


if __name__=="__main__":
    app.run(debug=True)