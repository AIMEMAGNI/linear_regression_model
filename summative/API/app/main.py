import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define the paths
model_path = os.path.join('app', 'linear_regression_model.pkl')
scaler_path = os.path.join('app', 'scaler.pkl')
poly_path = os.path.join('app', 'poly.pkl')
label_encoders_path = os.path.join('app', 'label_encoders.pkl')

# Load the model and the preprocessors
try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    poly = joblib.load(poly_path)
    label_encoders = joblib.load(label_encoders_path)
except Exception as e:
    raise ValueError(f"Error loading model or preprocessors: {e}")


class TVData(BaseModel):
    Brand: str
    Resolution: str
    Operating_System: str
    Size: float


@app.post("/predict")
def predict(data: TVData):
    try:
        encoded_data = [
            label_encoders['Brand'].transform([data.Brand])[0],
            label_encoders['Resolution'].transform([data.Resolution])[0],
            label_encoders['Operating System'].transform(
                [data.Operating_System])[0]
        ]
        features = encoded_data + [data.Size]
        features_poly = poly.transform([features])
        scaled_features = scaler.transform(features_poly)
        prediction = model.predict(scaled_features)
        return {"predicted_price": prediction[0]}
    except KeyError as e:
        raise HTTPException(
            status_code=400, detail=f"Missing or invalid feature: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Welcome to the TV price prediction API!"}


@app.get("/predict")
def predict_get():
    raise HTTPException(
        status_code=405, detail="Method Not Allowed. Use POST request.")
