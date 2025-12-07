import sqlite3

conn = sqlite3.connect('temps.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE temps (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        air_temperature REAL,
        apparent_temperature REAL,
        relative_humidity REAL,
        wind_speed REAL,
        maximum_gust REAL
    )
''')
conn.commit()
conn.close()