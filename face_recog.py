import cv2
import face_recognition
import threading
import time
import queue
from jarvis_config import Jarvis
import pygame
import os
from dotenv import load_dotenv
load_dotenv()

jarvis = Jarvis()
# Load the known images and encode their face landmarks
image= face_recognition.load_image_file(f'{os.getenv("IMAGE_OF_YOU")}')
face_encoding = face_recognition.face_encodings(image)[0]


# Create a list of known face encodings and names
known_face_encodings = [
    face_encoding
]

known_face_names = [
    f"{os.getenv('YOUR_NAME')}"
]


def face_recognition_thread(rgb_frame, face_locations, face_encodings, my_queue):
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        # If a match was found, add the name to the queue
        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]
            my_queue.put(name)
        
def facerec(face_scan_sound=False):
    # Initialize the webcam
    video_capture = cv2.VideoCapture(0)

    # Create a queue to hold the detected names
    my_queue = queue.Queue()
    
    # Set the detection timeout to 20 seconds
    detection_timeout = 20
    detection_start_time = time.time()
    
    jarvis.say("Initiating facial recognition. This process may take a moment.")
    if face_scan_sound:
        pygame.init()
        pygame.mixer.music.load(r'D:\OneDrive\Desktop\Jarvis\wakeword\facescansound.WAV')
        pygame.mixer.music.play()
    
    while True:
        # Get the current frame
        ret, frame = video_capture.read()

        # Convert the frame from BGR to RGB
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Run face recognition in a separate thread
        face_recognition_thread_obj = threading.Thread(target=face_recognition_thread, args=(rgb_frame, face_locations, face_encodings, my_queue))
        face_recognition_thread_obj.start()
        face_recognition_thread_obj.join()

        # Check if a name has been detected in the queue
        if not my_queue.empty():
            video_capture.release()
            name = my_queue.get()
            return name
        
        # Check if the detection timeout has been reached
        if time.time() - detection_start_time > detection_timeout:
            video_capture.release()
            return "unknown face"


        # Exit the program if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    video_capture.release()
    
    

