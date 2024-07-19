from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# import numpy as np
import joblib
import os

app = FastAPI()

# Define the paths
# current_directory = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join('linear_regression_model.pkl')
scaler_path = os.path.join('scaler.pkl')
poly_path = os.path.join('poly.pkl')
label_encoders_path = os.path.join('label_encoders.pkl')

# Load the model and the preprocessors
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    poly = joblib.load(poly_path)
    label_encoders = joblib.load(label_encoders_path)
except Exception as e:
    raise ValueError(f"Error loading model or preprocessors: {e}")

# Define the request body


class TVData(BaseModel):
    Brand: str
    Resolution: str
    Operating_System: str
    Size: float


@app.post("/predict")
def predict(data: TVData):
    try:
        # Encode the categorical features
        encoded_data = [
            label_encoders['Brand'].transform([data.Brand])[0],
            label_encoders['Resolution'].transform([data.Resolution])[0],
            label_encoders['Operating System'].transform(
                [data.Operating_System])[0]
        ]

        # Append the Size feature
        features = encoded_data + [data.Size]

        # Add polynomial features
        features_poly = poly.transform([features])

        # Scale the features
        scaled_features = scaler.transform(features_poly)

        # Make a prediction
        prediction = model.predict(scaled_features)

        return {"predicted_price": prediction[0]}
    except KeyError as e:
        raise HTTPException(
            status_code=400, detail=f"Missing or invalid feature: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# To run the app, use the following command in the terminal:
# uvicorn main:app --reload
