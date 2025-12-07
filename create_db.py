import sqlite3

conn = sqlite3.connect('temps.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE temps (
        id INTEGER PRIMARY KEY,
        timestamp TEXT,
        air_temperature REAL,
        apparent_temperature REAL,
        rel_humidity REAL,
        wind_spd_kmh REAL,
        maximum_gust_kmh REAL
    )
''')
conn.commit()
conn.close()