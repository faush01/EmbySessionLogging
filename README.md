## EmbySessionLogging

Emby server session logging will allow you to mointor what is happening on your Emby server. 
This can help detect load issues and overall server health. 

### Run the logging script

- Download and install python  
Windows python distribution Miniconda - https://docs.conda.io/projects/miniconda/en/latest/
- Download the python script emby_session_logging.py and save it locally
- In the Emby web client dashboard go to the API Keys area, create a new API key
- Open a command prompt in the path you download the script to and use the following command, replacing <api_key> with the key you just created:  
```python emby_session_logging.py <api_key>```

### Check logging

### Setup Grafana

### Grafana dashboard

- Create a new dashboard
- Add a visualization to the new dashboard
- In the data source drop down select the Sqlite data source create above
- Copy and paste the following query into the query area
- Click Apply, you now have a new chart with the logged session data

```
SELECT 
	event_date as ts, 
	CAST(json_extract(data, '$.t') AS FLOAT) as "Sessions",
	CAST(json_extract(data, '$.p') AS FLOAT) as "Playing",
	CAST(json_extract(data, '$.vt') AS FLOAT) as "VTrans",
	CAST(json_extract(data, '$.at') AS FLOAT) as "ATrans"
FROM session_log
WHERE event_date BETWEEN ${__from:date:seconds} AND ${__to:date:seconds}
GROUP BY 1 ORDER BY 1 ASC
```

