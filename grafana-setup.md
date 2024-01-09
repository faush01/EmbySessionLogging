## Grafana Chart Query

- Create a new dashboard
- Add a visualization
- In the data source drop down select you Sqlite data source
- Copy and past the following query in the query area
- Click Apply, you shold now have a new chart with the logged session data

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
