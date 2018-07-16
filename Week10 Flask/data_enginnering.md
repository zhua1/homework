

```python
import pandas as pd
```


```python
station = pd.read_csv('Resources\hawaii_stations.csv')
measurement = pd.read_csv('Resources\hawaii_measurements.csv').dropna()
```


```python
station.to_csv('Resources\cleaned_hawaii_stations.csv', index = False)
measurement.to_csv('Resources\cleaned_hawaii_measurements.csv', index = False)
```
