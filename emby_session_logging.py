import sys
import requests
import sqlite3
from contextlib import closing
import time
from datetime import datetime, timezone
import json

emby_url = "http://localhost:8096"

def session_info(sessions):
    s_info = {"as": 0, "p": 0, "vt": 0, "at": 0, "hvd": 0, "hve": 0}
    for session in sessions:
        #print(session)
        last_active = session["LastActivityDate"]  # "2020-07-18T04:08:53.1184838Z" "2024-01-13T02:40:01.2405182Z"
        last_active = last_active[0: last_active.index(".")] + "+0000"
        last_active = datetime.strptime(last_active, '%Y-%m-%dT%H:%M:%S%z')
        last_active_ago = (datetime.now(timezone.utc) - last_active).total_seconds()
        if last_active_ago < (5 * 60):
            s_info["as"] += 1
        if session.get("NowPlayingItem"):
            s_info["p"] += 1
            transcoding_info = session.get("TranscodingInfo")
            if transcoding_info:
                if transcoding_info.get("IsVideoDirect") is False:
                    s_info["vt"] += 1
                if transcoding_info.get("IsAudioDirect") is False:
                    s_info["at"] += 1
                if transcoding_info.get("VideoDecoderIsHardware"):
                    s_info["hvd"] += 1
                if transcoding_info.get("VideoEncoderIsHardware"):
                    s_info["hve"] += 1
    return s_info

def log_session_info(s_info):
    epoch_time = int(time.time())
    session_data = json.dumps(s_info)
    print("Logging session data: " + str(epoch_time) + " - " + session_data)
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

if len(sys.argv) != 2:
    print("Usage: python emby_session_logging.py <api_key>")
    print("or     python emby_session_logging.py dump")
    sys.exit(1)

create_table()

if sys.argv[1] == "dump":
    dump_table_data()
    sys.exit(0)

sessions_url = emby_url + "/emby/Sessions?api_key=" + sys.argv[1]

while True:
    try:
        response = requests.get(sessions_url)
        if response.status_code != 200:
            print("Error: " + str(response.status_code) + " - " + response.reason + " - " + response.text)
            break
        log_session_info(session_info(response.json()))
        time.sleep(60)
    except Exception as err:
        print("Error: " + str(err))
        break
