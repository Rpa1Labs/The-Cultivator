#DBs imports
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from sqlite3 import connect as sqlite3_connect

#flask imports
from flask import Flask , render_template, request
from flask_socketio import SocketIO

#other imports
import json
from datetime import datetime

#flask init
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret' #Pas bien
app.config['DEBUG'] = False
socketio = SocketIO(app)

#sqlite3 database
database = "data.db"


# InfluxDB database tokens and names
token = "b-6r8CDUz3QffJeawBtbxseUizxGGRrYaARD72RbxdFf4Occ_Y4T8-fH882nsPrrSdO7tgGupArG6jzW0RoJog=="
org = "Polytech"
bucket = "Environnement_measures"
bucket2="Image"
bddUrl = "http://54.36.191.243:8086"

"""
SQL Database
"""
def init():
    db = sqlite3_connect(database)
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS plants ( Id INTEGER UNIQUE, x INTEGER,y INTEGER,PRIMARY KEY(Id AUTOINCREMENT));")
    db.commit()
    db.close()
init()

def addPlant(x,y):
    db = sqlite3_connect(database)
    cur = db.cursor()
    cur.execute("INSERT INTO plants (x,y) VALUES (?,?)",(x,y))
    db.commit()
    db.close()

def getPlants():
    db = sqlite3_connect(database)
    cur = db.cursor()
    cur.execute("SELECT * FROM plants")
    plants = cur.fetchall()
    db.close()
    return plants

def getPlant(id):
    db = sqlite3_connect(database)
    cur = db.cursor()
    cur.execute("SELECT * FROM plants WHERE Id=?",(id,))
    plant = cur.fetchone()
    db.close()
    return plant


def deletePlant(id):
    db = sqlite3_connect(database)
    cur = db.cursor()
    cur.execute("DELETE FROM plants WHERE Id=?",(id,))
    db.commit()
    db.close()


"""
SocketIO
"""


# Soketio connection event
@socketio.on('connect')
def on_connect():
    print('Server received connection')

# Socketio disconnect event
@socketio.on('disconnect')
def on_disconnect():
    #TODO: manage disconnection for data acquisition triggering
    print('Client disconnected')

# Soketio message event
@socketio.on('dataTransmission')
def handle_message(msg):

    args = { 
        "AirHumidity":      "airhumidity airhumidityvalue=",
        "AirTemperature":   "temperature temperaturevalue=",
        "SoilMoisture":     "soilmoisture soilmoisturevalue="
    }

    #decode json
    print(msg)
    data = json.loads(msg)

    with InfluxDBClient(url=bddUrl, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        for measureType, value in data.items():
            try:
                data = str(args[measureType]) + str(value)
                print(data)
                write_api.write(bucket, org, data)
            except:
                print("Error when writing to the database")
        client.close()


#TODO: A revoir la fonction de transmission des images
@socketio.on('imageTransmission')
def write(msg):
    #decode json
    print(msg)
    data = json.loads(msg)
    print(data)
    with InfluxDBClient(url=bddUrl, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        #add image, plantid and surface area to influxdb
        data = "image imagevalue=" + data["image"] + " plantid=" + data["id"] + " surface=" + data["surface"]
        write_api.write(bucket2, org, data)
        #data = "image imagevalue="+msg 
        #write_api.write(bucket2, org, data)
        client.close()


"""
Acquisition trigger
"""

def launchAcquisition():
    print("Acquisition launched")
    #socketio.emit('dataTransmission', getLastMeasures())

def launchPlantAcquisition():
    print("Plant acquisition launched")
    #socketio.emit('dataTransmission', getLastPlantMeasures())

"""
HTTP WEB CLIENT PART
"""

def getLastMeasures():
    
    args = [ ["soilmoisture",   "soilmoisturevalue",    "Soil_Moisture"     ], 
             ["airhumidity",    "airhumidityvalue",     "Air_Humidity"      ], 
             ["temperature", "temperaturevalue",  "Air_Temperature"   ] ]

    results = {}

    try:
        with InfluxDBClient(url=bddUrl, token=token, org=org) as client:
            for parameters in args:
                print(parameters[0])
                #get last measure influxdb
                query = 'from(bucket: "' + bucket + '") |> range(start: 0) |> last() |> filter(fn:(r) => r._measurement == "' + parameters[0] + '" and r._field == "' + parameters[1] + '")'
                tables = client.query_api().query(query=query, org=org)
                print(tables)
                for table in tables :
                    for record in table.records:
                        results[parameters[2]] = record.get_value()
                        results["timestamp"] = int(record.get_time().timestamp())
            client.close()
    except:
        print("Error when reading from the database")
        
    return results

#index page
@app.route("/")
def home():
    data = getLastMeasures()
    #Moche mais fonctionne
    try:
        temperature = data["Air_Temperature"]
    except:
        temperature = "-"
    try:
        airHumidity = data["Air_Humidity"]
    except:
        airHumidity = "-"
    try:
        soilMoisture = data["Soil_Moisture"]
    except:
        soilMoisture = "-"
    try:
        timestamp = data["timestamp"]
        date = "Le " + datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y') + " à " + datetime.fromtimestamp(timestamp).strftime('%H:%M')
    except:
        pass

    #pas terrible mais pas de temps pour le moment
    xmax = 1030
    ymax = 328
    
    #TODO: faire un truc plus propre
    return render_template("./index.html" , AirTemperature = temperature, AirHumidity = airHumidity, SoilMoisture = soilMoisture, date=date, plants = getPlants(), xmax=xmax, ymax=ymax)

#settings page
@app.route("/settings")
def settings():

    #pas terrible mais pas de temps pour le moment
    xmax = 1030
    ymax = 328
    
    #TODO: faire un truc plus propre
    return render_template("./settings.html" , plants = getPlants(), xmax=xmax, ymax=ymax)


"""
HTTP API PART
"""

#API web client
@app.route("/webClientAPI", methods = ['POST'])
def WEBAPI():
    data = request.get_json()
    #get action
    action = data["action"]

    code = 200
    data_return = {}

    #No switch case in python :(
    if action == "getLastMeasures":
        data_return = getLastMeasures()
    elif action == "addPlant":
        addPlant(data["x"],data["y"])
        data_return = getPlants()
    elif action == "getPlants":
        data_return = getPlants()
    elif action == "getPlant":
        data_return = getPlant(data["id"])
    elif action == "launchAcquisition":
        launchAcquisition()
    elif action == "launchPlantAcquisition":
        launchPlantAcquisition()
    elif action == "deletePlant":
        #deletePlant(data["id"])
        #data_return = getPlants()
        pass
    elif action == "updatePlant":
        #updatePlant(data["id"],data["x"],data["y"])
        #data_return = getPlants()
        pass
    elif action == "getPlantDetails":
        #get plant details from database
        try:
            result = getPlant(data["id"])
            data_return = { "id": result[0], "x": result[1], "y": result[2], "surface" : 1000}
            #TODO: get surface area and image from influxdb
        except:
            code = 404
            data_return = "Plant not found"
    else:
        code = 400
        data_return = "Unknown action"

    return json.dumps(data_return), code , {'Content-Type':'application/json'}

#API AR HCI
@app.route('/HumiditySoil')
@app.route('/HumidityAir')
@app.route('/TemperatureAir')
def HCIAPI():
    #get url path on the header
    url = request.path

    # Get parameters corresponding to the url
    args = {    "/HumiditySoil"     : ["soilmoisture",   "soilmoisturevalue",    "Soil_moisture"     ], 
                "/HumidityAir"      : ["airhumidity",    "airhumidityvalue",     "Air_Humidity"      ], 
                "/TemperatureAir"   : ["temperature", "temperaturevalue",  "Air_Temperature"   ] }

    # Get the corresponding parameters to recover from influxdb
    try:
        parameters = args[url]
    except KeyError:
        return json.dumps({'error' : ["404 Not found"]}) , 404 , {'Content-Type':'application/json'}

    results=[]

    # Get the data from the database
    try:
        with InfluxDBClient(url=bddUrl, token=token, org=org) as client:
            query = 'from(bucket: "' + bucket + '") |> range(start: -3d) |> filter(fn:(r) => r._measurement == "' + parameters[0] + '" and r._field == "' + parameters[1] + '")'
            tables = client.query_api().query(query=query, org=org)
            for table in tables :
                for record in table.records:
                    results.append({"time" : str(record.get_time()),parameters[2]: str(record.get_value())})
            client.close()
        return json.dumps({"measures":results}) , 200 , {'Content-Type':'application/json'}
    except Exception as e:
        return json.dumps({'error' : ["500 Internal Server Error"]}) , 500 , {'Content-Type':'application/json'}





if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')
    socketio.run(app)
