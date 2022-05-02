
import base64
import cv2
import json
import sys
from imageProcessing import process_image

isConnected = False

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=1920,
    display_height=1080,
    framerate=1,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

def show_camera():
    # Start video stream
    video_capture = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

    # When the video capture object is created by OpenCV, it starts capturing
    if video_capture.isOpened():

        # Read one frame
        ret_val, image = video_capture.read()
        
        #convert to base64
        ret_val, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        
        # Close the video capture object
        video_capture.release()

        #return jpg_as_text
        return jpg_as_text,image
    else:
        print("Error: Unable to open camera")
    
    return None





def main(id=0,x=0,y=0):
    #TODO: Shift the camera to the right position
    #TODO: Process the image to get the surface area
    
    text_image,image = show_camera()
    surfaceArea = process_image(image)

    data= {"id":id,"image":text_image,"surface":surfaceArea}

    #TODO: faire une meilleure implémentation de la transmission de données

    print("##BEGIN DATA##")

    #print the data
    print(json.dumps(data))


if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])