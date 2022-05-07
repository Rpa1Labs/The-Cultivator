import socketio, board, adafruit_bme680, json
from adafruit_seesaw.seesaw import Seesaw

"""
DATA ACQUISITION
"""
#Init I2C
i2c=board.I2C()

#I2C adresses setup
bme680=adafruit_bme680.Adafruit_BME680_I2C(i2c,0x76)
ss=Seesaw(i2c,addr=0x36)

def getMeasurements():
    #Data acquisition
    temp=bme680.temperature
    airhum=bme680.relative_humidity
    soilmoisture=ss.moisture_read()

    #Values correction
    temp=temp-3
    airhum=airhum+5
    temp=round(temp,2)
    airhum=round(airhum,2)
    soilmoisturec=soilmoisture*100/2000
    soilmoisturec=round(soilmoisturec,2)
    return json.dumps({ "AirTemperature" : str(temp) , "AirHumidity" : str(airhum), "SoilMoisture" : str(soilmoisturec)})

"""
SOCKETIO CLIENT
"""

def sendData():
    #create socketio client
    sio = socketio.Client()

    #Server connection
    sio.connect('http://54.36.191.243:5000')

    #Send data to the server
    sio.emit("dataTransmission", getMeasurements())

    #Disconnect from the server
    sio.sleep(3)
    sio.disconnect()


if __name__ == "__main__":
    sendData()