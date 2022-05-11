
import socketio, socket, json,time,os
import subprocess
from measureAcquisition import getMeasurements

#run step motor process as root
os.system('./stepMotors/execStepper &')

#TODO: add a function to manage the stepper

def sendStepperCommand(c,m,d):
    
    #convert all values to binary
    command = int(c).to_bytes(2, 'little')
    motor = int(m).to_bytes(2, 'little')
    distance = int(d).to_bytes(4, 'little')

    #create 8 bytes value
    value = bytearray()
    value.extend(bytearray(distance))
    value.extend(bytearray(motor))
    value.extend(bytearray(command))

    #initialize socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 800))

    #send command
    s.send(value)

    #receive 1 byte
    code = int.from_bytes(s.recv(1), "big")
    s.close()
    return code

    

def manageStepper(x,y):

    #HOMING BOTH MOTORS
    if sendStepperCommand(0,0,0) >0:
        return False
    
    #delay 500ms
    time.sleep(0.5)

    if sendStepperCommand(0,1,0) >0:
        return False

    #SHIFTING BOTH MOTORS

    if sendStepperCommand(1,0,x) >0:
        return False
    if sendStepperCommand(1,1,y) >0:
        return False
    return True

    

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

    if manageStepper(x,y):
        result = subprocess.run(["python2", "./Acquisitions/imageAcquisition.py",str(id),"0","0"], stdout=subprocess.PIPE)
        substr = result.stdout.decode('utf-8')
        array = substr.split("\n")
        sio.emit("imageTransmission", array[array.index("##BEGIN DATA##")+1])
    else:
        print("Capture failed")
    
    return


@sio.on('measureTrigger')
def measureTrigger(data):
    print("measureTrigger")
    #execute function and get the result
    #moins crade que imageAcquisition.py
    result = getMeasurements()
    sio.emit("dataTransmission", result)

# Get web server url in config.json

URL = ""

with open('config.json') as json_file:
    data = json.load(json_file)
    URL = data['url']

print("Connecting to " + URL)

sio.connect(URL)
#run forever
while True:
    sio.wait()


