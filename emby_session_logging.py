import sys
import requests
import sqlite3
from contextlib import closing
import time
import json

api_key = "<api key from emby>"
sessions_url = "http://localhost:8096/emby/Sessions?api_key=" + api_key

def session_info(sessions):
    s_info = {"t": 0, "p": 0, "vt": 0, "at": 0}
    for session in sessions:
        s_info["t"] += 1
        if session.get("NowPlayingItem"):
            s_info["p"] += 1
            transcoding_info = session.get("TranscodingInfo")
            if transcoding_info:
                if transcoding_info.get("IsVideoDirect") is False:
                    s_info["vt"] += 1
                if transcoding_info.get("IsAudioDirect") is False:
                    s_info["at"] += 1
    return s_info

def log_session_info(s_info):
    epoch_time = int(time.time())
    session_data = json.dumps(s_info)
    with closing(sqlite3.connect('sessions.db')) as conn:
        with closing(conn.cursor()) as cursor:
            sql_insert = "INSERT INTO session_log (event_date, data) VALUES (?, ?)"
            cursor.execute(sql_insert, (epoch_time, session_data))
            conn.commit()

def create_table():
    with closing(sqlite3.connect('sessions.db')) as conn:
        with closing(conn.cursor()) as cursor:
            sql_create = "CREATE TABLE IF NOT EXISTS session_log ("
            sql_create += "event_date int NOT NULL, "
            sql_create += "data text, "
            sql_create += "PRIMARY KEY (event_date)"
            sql_create += ")"
            cursor.execute(sql_create)
            conn.commit()

def dump_table_data():
    with closing(sqlite3.connect('sessions.db')) as conn:
        with closing(conn.cursor()) as cursor:
            sql_select = "SELECT * FROM session_log"
            cursor.execute(sql_select)
            for row in cursor:
                print(row)

create_table()

if len(sys.argv) == 2 and sys.argv[1] == "dump":
    dump_table_data()
    sys.exit(0)

while True:
    response = requests.get(sessions_url)
    log_session_info(session_info(response.json()))
    time.sleep(60)
