import numpy as np
import cv2
import tensorflow as tf
import keras
from keras.models import load_model


# Load the face detection model
face_detection = cv2.CascadeClassifier(r'D:\OneDrive\Desktop\Jarvis\face_expression_config\haar_cascade_face_detection.xml')

# Load the expression recognition model and labels
model = load_model(r'D:\OneDrive\Desktop\Jarvis\face_expression_config\network-5Labels.h5')
labels = ['Surprise', 'Neutral', 'Anger', 'Happy', 'Sad']

def detect_expression():

		camera = cv2.VideoCapture(0)
		camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
		camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
		settings = {
			'scaleFactor': 1.3, 
			'minNeighbors': 5, 
			'minSize': (50, 50)
		}

		labels = ['Surprise', 'Neutral', 'Anger', 'Happy', 'Sad']

		while True:
			ret, img = camera.read()
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			detected = face_detection.detectMultiScale(gray, **settings)
			
			for x, y, w, h in detected:
				cv2.rectangle(img, (x, y), (x+w, y+h), (245, 135, 66), 2)
				cv2.rectangle(img, (x, y), (x+w//3, y+20), (245, 135, 66), -1)
				face = gray[y+5:y+h-5, x+20:x+w-20]
				face = cv2.resize(face, (48,48)) 
				face = face/255.0
				
				predictions = model.predict(np.array([face.reshape((48,48,1))])).argmax()
				state = labels[predictions]
				
				if state == "Surprise":
					return "Surprise"
				if state == "Neutral":
					return "Neutral"
				if state == "Anger":
					return "Anger"
				if state == "Happy":
					return "Happy"
				if state == "Sad":
					return "Sad"

			if cv2.waitKey(5) != -1:
				break

		camera.release()


