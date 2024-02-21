import os
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import cv2
import numpy as np

app = Flask(__name__)

# Load your trained model
alzheimer_model = load_model("C:/Users/srini/OneDrive/Documents/new project/Server-side/ml_model/alzheimer_model.h5")

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (32, 32))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.reshape(32, 32, 1)
    return img

@app.route('/')
def index():
    return "Welcome to Alzheimer's Prediction API!"

@app.route('/predictAlzheimer', methods=['POST'])
def predict_alzheimer():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Process the image for prediction
    image_path = "C:/Users/srini/OneDrive/Documents/6TH SEM/DSAI/project/Alzheimer_s Dataset/test/MildDemented/26 (23).jpg"
    file.save(image_path)
    processed_image = preprocess_image(image_path)

    try:
        # Make predictions using the model
        prediction = alzheimer_model.predict(np.expand_dims(processed_image, axis=0))
        # Get the predicted class label
        predicted_class_index = np.argmax(prediction)
        # Map the predicted class index to the corresponding class label
        class_labels = ["Demented", "Mild Demented", "Moderate Demented", "Very Mild Demented"]
        predicted_class = class_labels[predicted_class_index]

        # Return the predicted class to the frontend
        return jsonify({'result': predicted_class})

    except Exception as e:
        # Log the error for debugging
        print("Error predicting Alzheimer's:", e)
        return jsonify({'error': 'Error predicting Alzheimer\'s'})

if __name__ == '__main__':
    app.run(debug=True)
