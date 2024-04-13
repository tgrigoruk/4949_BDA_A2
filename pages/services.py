import pandas as pd
import joblib
import torch
import numpy as np
from django.conf import settings
from pathlib import Path

PATH = settings.BASE_DIR / Path("static/binaries")

SCALER = joblib.load(PATH / "scaler.joblib")
MODEL = joblib.load(PATH / "model_rf.joblib")


def prepare_data(raw_data):
    data = {}
    
    data["Class_Business"] = 1 if raw_data["Class"] == "Business" else 0
    data["Type of Travel_Personal Travel"] = (
        1 if raw_data["Type of Travel"] == "Personal Travel" else 0
    )

    data["Age_40-60"] = 1 if 38 < raw_data["Age"] < 60 else 0

    data["Seat comfort"] = raw_data["Seat comfort"]
    data["Leg room service"] = raw_data["Leg room service"]

    data["Inflight entertainment"] = raw_data["Inflight entertainment"]
    data["Inflight wifi service"] = raw_data["Inflight wifi service"]

    data["Online boarding"] = raw_data["Online boarding"]
    data["On-board service"] = raw_data["On-board service"]

    df = pd.DataFrame(data, index=[0])
    return df


def get_prediction(data):
    data_prepared = prepare_data(data)
    print(data_prepared)
    data_scaled = SCALER.transform(data_prepared)
    print(data_scaled)
    prediction = MODEL.predict(data_scaled)
    print(prediction)
    return prediction[0]
