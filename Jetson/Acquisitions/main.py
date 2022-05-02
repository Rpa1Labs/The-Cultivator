
import socketio
import subprocess
from measureAcquisition import getMeasurements

sio = socketio.Client()
execution=0
@sio.on('connect')
def on_connect():
    sio.emit("setupTrigger", "")


@sio.on('imageTrigger')
def imageTrigger():
    #execute external script and get the result
    #extrèmement crade, mais c'est pour le moment
    result = subprocess.run(["python2", "imageAcquisition.py","0","0","0"], stdout=subprocess.PIPE)
    substr = result.stdout.decode('utf-8')
    array = substr.split("\n")
    sio.emit("imageTransmission", array[array.index("##BEGIN DATA##")+1])


@sio.on('measureTrigger')
def measureTrigger():
    #execute function and get the result
    #moins crade que imageAcquisition.py
    result = getMeasurements()
    sio.emit("dataTransmission", result)


sio.connect('http://192.168.31.235:5000')
#run forever
while True:
    sio.wait()


