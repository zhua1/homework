

```python
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, Text, Float, Integer
```


```python
station = pd.read_csv('Resources\cleaned_hawaii_stations.csv')
measurement = pd.read_csv('Resources\cleaned_hawaii_measurements.csv')
```


```python
engine = create_engine("sqlite:///hawaii.sqlite", echo = False)
conn = engine.connect()
Base = declarative_base()

class Station(Base):
    __tablename__ = 'stations'
    
    id = Column(Integer, primary_key=True)
    station = Column(Text)
    name = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    
class Measurement(Base):
    __tablename__ = 'measurements'
    
    id = Column(Integer, primary_key=True)
    station = Column(Text)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Integer)
```


```python
station.to_sql('stations', conn, dtype={'id': Integer(), 'station': Text(), 'name': Text(), 
                                        'latitude': Float(), 'longitude': Float(), 'elevation': Float()})
measurement.to_sql('measurements', conn, dtype={'id': Integer(), 'station': Text(), 'date': Text(), 'prcp': Float(), 
                                                'tobs': Integer()})
```
