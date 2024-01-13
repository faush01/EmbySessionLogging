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
- The script logs session data to a Sqlite DB file sessions.db in the same dir as the script is run
- The script will not exit, it will run forever logging the Emby session info every 60 seconds

### Check logging

- Open a command prompt and run the script with the dump option:  
```python emby_session_logging.py dump```
- This will dump all the logged data to the console

### Setup Grafana

- Download the latest version of Grafana:  
https://grafana.com/grafana/download
- After installation install the SQLite Datasource plugin:  
https://grafana.com/grafana/plugins/frser-sqlite-datasource/
- Start up and verify Grafana is working and you can see the interface:  
http://localhost:3000

### Setup datasource

- In Grafana create a new data source connection in Grafana
- Click the 3 bars, top left, to bring up the menu
- Click Connections and then click data sources, in the top right click "+ Add new data source" 
- Enter Sqlite in the search box enter Sqlite
- You should see the Sqlite data source plugin, if you dont then it is not install correctly go back and work out why
- Click the Sqlite data source plugin
- Give your data source a name in the name field, something like "emby_sessions"
- You need to fill in the path to the sessions.db file created when running the logging script

### Grafana dashboard

- Create a new dashboard
- Add a visualization to the new dashboard
- In the data source drop down select the Sqlite data source create above
- Copy and paste the following query into the query area
- Click Apply, you now have a new chart with the logged session data

```
SELECT 
	event_date as ts, 
	CAST(json_extract(data, '$.as') AS FLOAT) as "Active",
	CAST(json_extract(data, '$.p') AS FLOAT) as "Playing",
	CAST(json_extract(data, '$.vt') AS FLOAT) as "VTrans",
	CAST(json_extract(data, '$.at') AS FLOAT) as "ATrans",
	CAST(json_extract(data, '$.hvd') AS FLOAT) as "HwDecode",
	CAST(json_extract(data, '$.hve') AS FLOAT) as "HwEncode"	
FROM session_log
WHERE event_date BETWEEN ${__from:date:seconds} AND ${__to:date:seconds}
GROUP BY 1 ORDER BY 1 ASC
```

