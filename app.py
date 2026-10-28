import joblib
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="California Housing Price Prediction API")

model = joblib.load("model.joblib")


class HousingFeatures(BaseModel):
    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


@app.get("/")
def health_check():
    return {"status": "ok", "service": "California Housing Price API"}


@app.post("/predict")
def predict_price(features: HousingFeatures):
    input_data = np.array(
        [[
            features.MedInc,
            features.HouseAge,
            features.AveRooms,
            features.AveBedrms,
            features.Population,
            features.AveOccup,
            features.Latitude,
            features.Longitude,
        ]]
    )

    # Output target is in $100,000s
    predicted_val = float(model.predict(input_data)[0])
    estimated_usd = round(predicted_val * 100000, 2)

    return {
        "predicted_unit_value": round(predicted_val, 4),
        "estimated_price_usd": estimated_usd,
    }