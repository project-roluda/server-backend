from flask import Flask, request
import joblib
import numpy as np
import requests
from src.shared import global_dict
from src.prediction import Patient
import time

import json as json_lib

app = Flask(__name__)

result_proba_dict = global_dict

@app.route("/", methods=["GET"])
def home():
    return result_proba_dict

@app.route("/override_result_dict", methods=["GET", "POST"])
def override_result_dict():
    global result_proba_dict
    json = request.get_json(force=True)
    result_proba_dict = json
    return "done", 200

@app.route("/process_audio", methods=["GET", "POST"])
def process_audio():
    global result_proba_dict
    json = request.get_json(force=True)
    print(json["avgCoeff"])

    avg_initial_coeff = np.array(json["avgCoeff"])

    patient = Patient()
    diagnostic_prediction = patient.post_data_to_azure(avg_initial_coeff)

    result_proba_dict["diagnostics"] = diagnostic_prediction
    result_proba_dict["status"] = "result"

    list_of_classes = list(diagnostic_prediction.keys())
    max_class = list_of_classes[0]

    for key in list_of_classes:
        if diagnostic_prediction[key] > diagnostic_prediction[max_class]:
            max_class = key 

    treatments = json_lib.load(open("static/treatments.json", 'r'))
    result_proba_dict["treatment"] = treatments[max_class]

    return "done"


@app.route("/reset", methods=["GET", "POST"])
def reset():
    result_proba_dict["status"] = "standby"
    result_proba_dict["displayText"] = "Welcome to Inspire"
    return "done"

@app.route("/camera", methods=["GET", "POST"])
def camera():
    result_proba_dict["status"] = "move_camera"
    result_proba_dict["displayText"] = "Please move within camera frame"
    return "done"

@app.route("/arm_extension", methods=["GET", "POST"])
def arm_extension():
    result_proba_dict["status"] = "arm"
    result_proba_dict["displayText"] = "Arm calibration"
    return "done"

@app.route("/inhale", methods=["GET", "POST"])
def inhale():
    result_proba_dict["status"] = "breathe"
    result_proba_dict["displayText"] = "Inhale"
    return "done"

@app.route("/exhale", methods=["GET", "POST"])
def exhale():
    result_proba_dict["status"] = "breathe"
    result_proba_dict["displayText"] = "Exhale"
    return "done"

@app.route("/set_processing", methods=["GET", "POST"])
def set_processing():
    result_proba_dict["status"] = "process"
    result_proba_dict["displayText"] = "Processing data..."
    return "done"

@app.route("/respiration", methods=["GET", "POST"])
def respiration():
    result_proba_dict["status"] = "breathe"
    for i in range(3):
        result_proba_dict["displayText"] = "Inhale"
        time.sleep(1.5)
        result_proba_dict["displayText"] = "Exhale"
        time.sleep(1.5)
    result_proba_dict["status"] = "processing"
    result_proba_dict["displayText"] = "Processing data ..."
    return "done"

@app.route("/show_status", methods=["GET"])
def show_status():
    return "200"

if __name__ == "__main__":
    app.run()
