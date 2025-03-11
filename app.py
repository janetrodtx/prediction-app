from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model and scaler
with open("models/stroke_risk_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("models/scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get data from form
        gender = int(request.form["gender"])
        age = float(request.form["age"])
        hypertension = int(request.form["hypertension"])
        heart_disease = int(request.form["heart_disease"])
        previous_stroke = int(request.form["previous_stroke"])
        ever_married = int(request.form["ever_married"])
        residence_type = int(request.form["residence_type"])
        avg_glucose_level = float(request.form["avg_glucose_level"])
        bmi = float(request.form["bmi"])

        # One-hot encoding for smoking status
        smoking_status = request.form["smoking_status"]
        smoking_encoded = [0, 0, 0]
        if smoking_status == "formerly_smoked":
            smoking_encoded[0] = 1
        elif smoking_status == "never_smoked":
            smoking_encoded[1] = 1
        elif smoking_status == "smokes":
            smoking_encoded[2] = 1

        # One-hot encoding for work type
        work_type = request.form["work_type"]
        work_encoded = [0, 0, 0, 0]
        if work_type == "Never_worked":
            work_encoded[0] = 1
        elif work_type == "Private":
            work_encoded[1] = 1
        elif work_type == "Self-employed":
            work_encoded[2] = 1
        elif work_type == "children":
            work_encoded[3] = 1

        # Prepare input
        input_data = np.array([[
            gender, age, hypertension, heart_disease, previous_stroke, ever_married, residence_type,
            avg_glucose_level, bmi
        ] + smoking_encoded + work_encoded]).reshape(1, -1)

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict risk score
        risk_score = model.predict_proba(input_scaled)[0][1] * 100

        return render_template("index.html", risk_score=round(risk_score, 2))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
