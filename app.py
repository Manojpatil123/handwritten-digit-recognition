from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
import os
from PIL import Image
from tensorflow.keras.preprocessing import image
import io
import base64
import mysql.connector
from functools import wraps
import json


BASE_DIR = os.getcwd()

app = Flask(__name__,template_folder="template",static_folder="static")
app.secret_key = '123456'  # Replace with a strong secret key
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder to store uploaded images

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Access database credentials and secret key from the config
db_config = config.get('database', {})
app.config['API_TOKEN']  = config.get('secret_key')


# Function to create database and table if they don't exist

def create_database_table():
    mydb = mysql.connector.connect(
        host=db_config.get('host'),
        user=db_config.get('user'),
        password=db_config.get('password'),
        database=db_config.get('database')
    )
    cursor = mydb.cursor()

    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS logs")
    cursor.execute("USE logs")

    # Create 'prediction_logs' table if it doesn't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS prediction_logs (\
        id INT AUTO_INCREMENT PRIMARY KEY,\
        input_type VARCHAR(10),\
        input_data TEXT,\
        prediction INT,\
        probabilities TEXT\
    )")

    mydb.commit()
    mydb.close()

create_database_table()  # Call function to create database and table

#connecting mysql with databse 
mydb = mysql.connector.connect(
        host=db_config.get('host'),
        user=db_config.get('user'),
        password=db_config.get('password'),
        database=db_config.get('database')
    )
cursor = mydb.cursor()
# Load the pre-trained MNIST model
model = tf.keras.models.load_model(BASE_DIR+'/data/best_model.h5')
#model._make_predict_function()  # Necessary for using the model in Flask

# Function to preprocess image for model prediction
def preprocess_image(img):
    # Convert image to grayscale and resize to 28x28
    img = img.convert('L').resize((28, 28))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array / 255.0 

# Authentication function
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token or token != app.config['API_TOKEN']:
            return jsonify({'message': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
@requires_auth
def classify():
    try:
        data = request.get_json()
        base64Image = data['image']
        
        img = Image.open(io.BytesIO(base64.b64decode(base64Image)))
        processed_img = preprocess_image(img)
        prediction = model.predict(processed_img)
        predicted_class = np.argmax(prediction[0])
        print(predicted_class)

        # Save prediction details to MySQL database
        cursor = mydb.cursor()
        sql = "INSERT INTO prediction_logs (input_type, input_data, prediction, probabilities) VALUES (%s, %s, %s, %s)"
        val = ('base64', base64Image, int(predicted_class), str(max(prediction[0])))
        cursor.execute(sql, val)
        mydb.commit()
        return jsonify({'prediction': str(predicted_class)})
    except Exception as e:
        return jsonify({'Error': str(e)})

@app.route('/classify_file', methods=['POST'])
@requires_auth
def classify_file():
    try:
        if 'file' not in request.files:
            return jsonify({'Error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'Eerror': 'No selected file'})

        if file:
            img = Image.open(file.stream)
            processed_img = preprocess_image(img)
            prediction = model.predict(processed_img)
            predicted_class = np.argmax(prediction[0])
            print(predicted_class)
            # Save prediction details to MySQL database
            cursor = mydb.cursor()
            sql = "INSERT INTO prediction_logs (input_type, input_data, prediction, probabilities) VALUES (%s, %s, %s, %s)"
            val = ('file', file.filename, predicted_class, str(max(prediction[0])))
            cursor.execute(sql, val)
            mydb.commit()

            return jsonify({'prediction': str(predicted_class)})

        return jsonify({'Error': 'Invalid file format'})
    except Exception as e:
        return jsonify({'Error': str(e)})

if __name__ == '__main__':
    app.run(debug=True,port=80)
