
# TV Price Prediction Project

This repository contains a TV Price Prediction project that consists of three main components: a machine learning model, a FastAPI backend, and a Flutter frontend.

## Project Structure

```
summative/
├── API/
├── flutter_app/
└── linear_regression/
```

### 1. API

The `API` directory contains the FastAPI backend that serves the machine learning model and handles prediction requests.

#### Key Files
- `app/`
  - `main.py`: The main FastAPI application file.
  - `linear_regression_model.pkl`: The trained linear regression model.
  - `scaler.pkl`: The scaler used for preprocessing.
  - `poly.pkl`: The polynomial features transformer.
  - `label_encoders.pkl`: The label encoders for categorical features.
  - Other necessary files for model loading and preprocessing.

#### How to Run Locally

1. Navigate to the `API` directory.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Start the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```

### 2. flutter_app

The `flutter_app` directory contains the Flutter frontend application that allows users to input TV features and get price predictions.

#### Key Files
- `lib/`
  - `main.dart`: The main entry point of the Flutter application.

#### How to Run

1. Ensure you have Flutter installed on your system.
2. Navigate to the `flutter_app` directory.
3. Get the Flutter dependencies:
    ```bash
    flutter pub get
    ```
4. Run the Flutter application:
    ```bash
    flutter run
    ```

### 3. linear_regression

The `linear_regression` directory contains the Jupyter notebooks and scripts used for training and evaluating the machine learning model.

#### Key Files
- `notebooks/`
  - `train_model.ipynb`: The notebook used for training the linear regression model.
  - `evaluate_model.ipynb`: The notebook used for evaluating the model.

#### How to Use

1. Navigate to the `linear_regression` directory.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Open the Jupyter notebooks to train and evaluate the model:
    ```bash
    jupyter notebook
    ```

## Usage

### FastAPI Backend

The FastAPI backend is deployed on Render and provides an endpoint for predicting TV prices based on input features. The endpoint is:

- `POST /predict`: Predicts the price of a TV given its features.

Example request:

```bash
curl -X POST "https://tv-prices-api.onrender.com/predict" -H "Content-Type: application/json" -d '{
  "Brand": "SAMSUNG",
  "Resolution": "Ultra HD LED",
  "Operating_System": "Android",
  "Size": 30
}'
```

### Flutter Frontend

The Flutter application provides a user-friendly interface for inputting TV features and displaying the predicted price.

Make sure the FastAPI backend URL in the Flutter application is set to the correct Render address:

```dart
final String apiUrl = 'https://tv-prices-api.onrender.com/predict';
```