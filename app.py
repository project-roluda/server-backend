from flask import Flask, request
import joblib
import librosa
import numpy as np

app = Flask(__name__)

result_proba_dict = {}

@app.route("/", methods=["GET"])
def home():
    return result_proba_dict

@app.route("/process_audio", methods=["POST"])
def process_audio():
    global result_proba_dict
    json = request.json
    print(json["avgCoeff"])

    avg_initial_coeff = np.array(json["avgCoeff"])
    ml_model = joblib.load("static/knn.sav")

    """
    audio_file = request.files["file"]
    audio_file.save("static/sample_audio.wav")


    sound, sample_rate = librosa.load("static/sample_audio.wav")
    initial_coeff = librosa.feature.mfcc(y=sound, sr=sample_rate, n_mfcc=100)
    avg_initial_coeff = np.mean(initial_coeff, axis=1)
    """

    res = ml_model.predict_proba([avg_initial_coeff])

    labels = ml_model.classes_

    result_proba_dict = {}

    print(labels)

    for i in range(len(labels)):
        result_proba_dict[labels[i]] = res[0][i]

    return result_proba_dict


@app.route("/show_status", methods=["GET"])
def show_status():
    return "200"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)