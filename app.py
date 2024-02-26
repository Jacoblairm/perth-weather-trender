from flask import Flask, render_template, jsonify, request
import ftplib
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from xml.etree import ElementTree as ET

app = Flask(__name__)

def scrape_and_store():
    ftp = ftplib.FTP('ftp.bom.gov.au')
    ftp.login()
    ftp.cwd('/anon/gen/fwo/')
    ftp.retrbinary('RETR IDW60920.xml', open('IDW60920.xml', 'wb').write)
    ftp.quit()

    tree = ET.parse('IDW60920.xml')
    root = tree.getroot()

    for station in root.iter('station'):
        if station.attrib['stn-name'] == "PERTH METRO":
            for period in station.iter('period'):
                timestamp = period.attrib['time-local']
                for level in period.iter('level'):
                    for element in level.iter('element'):
                        if element.attrib['type'] == 'air_temperature':
                            air_temperature = element.text
                        elif element.attrib['type'] == 'apparent_temp':
                            apparent_temp = element.text
                        elif element.attrib['type'] == 'rel-humidity':
                            rel_humidity = element.text
                        elif element.attrib['type'] == 'wind_spd_kmh':
                            wind_spd_kmh = element.text
                        elif element.attrib['type'] == 'gust_kmh':
                            gust_kmh = element.text

                conn = sqlite3.connect('temps.db')
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO temps (timestamp, air_temperature, apparent_temperature, relative_humidity, wind_speed, maximum_gust) VALUES (?, ?, ?, ?, ?, ?)", 
                          (timestamp, air_temperature, apparent_temp, rel_humidity, wind_spd_kmh, gust_kmh))
                conn.commit()
                conn.close()
            break

# Call the function on app start
scrape_and_store()

scheduler = BackgroundScheduler()
scheduler.add_job(scrape_and_store, 'interval', minutes=1)
scheduler.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
    limit = request.args.get('limit', default = 144, type = int)
    conn = sqlite3.connect('temps.db')
    c = conn.cursor()
    c.execute('SELECT * FROM temps ORDER BY id DESC LIMIT ?', (limit,))
    data = c.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)