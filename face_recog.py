import threading
import cv2
import face_recognition
import pyttsx3
import time


def facerec():

    # Load the known images and encode their face landmarks

    # Tyler
    image_of_tyler = face_recognition.load_image_file(r"C:\Users\tyler\iCloudDrive\Desktop\Jarvis\wakeword\known_faces\Tyler.jpg")
    tyler_face_encoding = face_recognition.face_encodings(image_of_tyler)[0]

    # elon
    image_of_elon = face_recognition.load_image_file(r"C:\Users\tyler\iCloudDrive\Desktop\Jarvis\wakeword\known_faces\elon.jpg")
    elon_face_encoding = face_recognition.face_encodings(image_of_elon)[0]

    image_of_elise = face_recognition.load_image_file(r"C:\Users\tyler\iCloudDrive\Desktop\Jarvis\wakeword\known_faces\elise.jpg")
    elise_face_encoding = face_recognition.face_encodings(image_of_elise)[0]

    # Create a list of known face encodings
    known_face_encodings = [
        tyler_face_encoding,
        elon_face_encoding,
        elise_face_encoding
    ]

    # Create a list of known face names
    known_face_names = [
        "Tyler",
        "Elon",
        "Elise"
    ]

    # Initialize the webcam
    video_capture = cv2.VideoCapture(0)

    # flag to indicate if a name has been detected
    name_detected = False
    
    # Start the timer
    start_time = time.time()
    while not name_detected:

        # Get the current frame
        ret, frame = video_capture.read()

        # Convert the frame from BGR to RGB
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in the current frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # If a match was found, return the name
            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]

                # set the flag variable to True
                name_detected = True

                # Release the webcam and close the window
                video_capture.release()
                return name
        # Check if the timer has exceeded 10 seconds
        if time.time() - start_time > 5:
            return "Tyler"
        
        # Exit the program if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    video_capture.release()