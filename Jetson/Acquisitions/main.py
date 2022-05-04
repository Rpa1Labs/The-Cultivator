
import socketio, socket, json,time
import subprocess
from measureAcquisition import getMeasurements

#TODO: add a function to manage the stepper

def manageStepper(x,y):
    command = 1
    command = command.to_bytes(2, 'little')
    motorx = 0
    motorx = motorx.to_bytes(2, 'little')
    motory = 1
    motory = motory.to_bytes(2, 'little')
    
    distancex = int(x).to_bytes(4, 'little')
    distancey = int(y).to_bytes(4, 'little')

    #extrèmement crade, mais ça marche
    #TODO: le refaire proprement

    #HOMING BOTH MOTORS
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 800))
    #send command
    #create 8 bytes value
    value = bytearray()
    for i in range(8):
        value.append(0)
    s.send(value)
    #receive 1 byte
    code = s.recv(1)
    s.close()

    #delay 500ms
    time.sleep(0.5)


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 800))
    #send command
    #create 8 bytes value
    value = bytearray()
    for i in range(8):
        value.append(0)
    value[4] = 1
    s.send(value)
    #receive 1 byte
    code = s.recv(1)
    s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 800))
    #send command
    #create 8 bytes value
    value = bytearray()
    value.extend(bytearray(distancex))
    value.extend(bytearray(motorx))
    value.extend(bytearray(command))

    s.send(value)
    #receive 1 byte
    code = s.recv(1)
    s.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 800))
    #send command
    #create 8 bytes value
    value = bytearray()
    value.extend(bytearray(distancey))
    value.extend(bytearray(motory))
    value.extend(bytearray(command))

    s.send(value)
    #receive 1 byte
    code = s.recv(1)
    s.close()

sio = socketio.Client()
execution=0
@sio.on('connect')
def on_connect():
    sio.emit("setupTrigger", "")


@sio.on('imageTrigger')
def imageTrigger(data):
    #execute external script and get the result
    #extrèmement crade, mais c'est pour le moment
    #connect to socket

    #decode the data
    data = json.loads(data)

    id=data["id"]

    print("imageTrigger")

    x = int(data["x"])
    y = int(data["y"])

    manageStepper(x,y)

    result = subprocess.run(["python2", "imageAcquisition.py",str(id),"0","0"], stdout=subprocess.PIPE)
    substr = result.stdout.decode('utf-8')
    array = substr.split("\n")
    sio.emit("imageTransmission", array[array.index("##BEGIN DATA##")+1])


@sio.on('measureTrigger')
def measureTrigger(data):
    print("measureTrigger")
    #execute function and get the result
    #moins crade que imageAcquisition.py
    result = getMeasurements()
    sio.emit("dataTransmission", result)


sio.connect('http://192.168.81.221:5000')
#run forever
while True:
    sio.wait()


