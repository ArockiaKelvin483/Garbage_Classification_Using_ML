from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
# Load the trained model
model = load_model('Garbage.h5')

# Define the Flask app
app = Flask(__name__)

# Define route for the home page
@app.route('/file')
def home():
    print("homee.......")
    return render_template('GC.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=["GET", "POST"])
def res():
    if request.method == "POST":
        f = request.files['image']
        filename = secure_filename(f.filename)
        filepath = filename
        f.save(filepath)

        img = image.load_img(filepath, target_size=(64, 64))  # Resize the image to (64, 64)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        prediction = model.predict(x)
        predicted_class_index = np.argmax(prediction)
        classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        predicted_class = classes[predicted_class_index]
        print(predicted_class)

        return render_template('result.html', prediction=predicted_class)
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)