from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import numpy as np

app = Flask(__name__)

dic = {0 : 'Vigne avec Esca', 1 : 'Vigne saine'}

model = tf.keras.models.load_model('model_voltron.h5')
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.make_predict_function()

def predict_label(img_path):
    i = tf.keras.preprocessing.image.load_img(img_path, target_size=(320,180))
    i = np.asarray(i)
    i = i.reshape(1, 320,180,3)
    p = model.predict_classes(i)    
    return dic[p[0]]

    

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ == "__main__":
    # use 0.0.0.0 to use it in container
    app.run(host='0.0.0.0')
