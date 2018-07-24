# 0. import dependencies
import pandas as pd
from flask import Flask
from flask import jsonify
from sqlalchemy import create_engine

#0. load data
engine = create_engine("sqlite:///hawaii.sqlite", echo = False)
conn = engine.connect()
station_df = pd.DataFrame(conn.execute('SELECT station FROM stations').fetchall())
station_df.columns = ['station']
_ = conn.execute('SELECT date, station, tobs \
                  FROM measurements \
                  WHERE date >= \'2016-08-23\' AND station == \'USC00519397\' \
                  GROUP BY date, station').fetchall()
tobs_df = pd.DataFrame(_)
tobs_df.columns = ['date', 'station', 'tobs']
temperature_data = pd.read_sql('measurements', conn, parse_dates={'date': {'format': '%Y-%m-%d'}}, columns=['date', 'tobs'])

# 0. Create app
app = Flask(__name__)

# 0. Initialize content page
@app.route('/')
def Welcome():
    return (
        f"Welcome to this API!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
        )

# 1. precipitation
@app.route('/api/v1.0/precipitation')
def Precipitation():
    precipitation = tobs_df[['date', 'tobs']]
    precipitation_table = []
    for i in range(precipitation.shape[0]):
        dic = {}
        dic['date'] = precipitation.date[i]
        dic['tobs'] = int(precipitation.tobs[i])
        precipitation_table.append(dic)
    return(jsonify(precipitation_table))

# 2. Station
@app.route('/api/v1.0/stations')
def Station():
    return(jsonify(station_df.to_dict()))

# 3. Tobs
@app.route('/api/v1.0/tobs')
def Tobs():
    tobs = tobs_df[['tobs']]
    return(jsonify(tobs.to_dict()))
    
# 4. Temperature
@app.route('/api/v1.0/<start>')
def show_start(start):
    def calc_temps(start_date):
        df = temperature_data[temperature_data.date >= start_date]
        dic = {}
        dic['min'] = df.tobs.min()
        dic['avg'] = df.tobs.mean()
        dic['max'] = df.tobs.max()
        return(dic)
    temps = calc_temps(start)
    di = {}
    di['TMIN'] = float(temps['min'])
    di['TAVG'] = float(temps['avg'])
    di['TMAX'] = float(temps['max'])
    return(jsonify(di))

@app.route('/api/v1.0/<start>/<end>')
def show_start_end(start, end):
    def calc_temps(start_date, end_date):
        df = temperature_data[(temperature_data.date >= start_date) & (temperature_data.date <= end_date)]
        dic = {}
        dic['min'] = df.tobs.min()
        dic['avg'] = df.tobs.mean()
        dic['max'] = df.tobs.max()
        return(dic)
    temps = calc_temps(start, end)
    di = {}
    di['TMIN'] = float(temps['min'])
    di['TAVG'] = float(temps['avg'])
    di['TMAX'] = float(temps['max'])
    return(jsonify(di))

# 5. Run App
if __name__ == '__main__':
    app.run(port = 5000, debug=True)