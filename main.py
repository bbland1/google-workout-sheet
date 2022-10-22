import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NUTRITION_APP_ID = os.getenv("NUTRITION_APPLICATION_ID")
NUTRITION_APP_KEY = os.getenv("NUTRITION_APPLICATION_KEY")
NUTRITION_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEET_ENDPOINT = os.getenv("SHEETY_ENDPOINT")
SHEET_AUTHENTICATION = os.getenv("SHEETY_AUTHENTICATION")

exercise = input("What exercise did you complete? ")

nutrition_header = {
   "x-app-id": NUTRITION_APP_ID,
    "x-app-key": NUTRITION_APP_KEY,
    "Content-Type": "application/json"
}

nutrition_params = {
    "query": exercise,
    "gender": "female",
    "weight_kg": float(90.72),
    "height_cm": float(165.1),
    "age": int(28),
}

nutrition_response = requests.post(url=NUTRITION_ENDPOINT, headers=nutrition_header, json=nutrition_params)
nutrition_response.raise_for_status()

nutrition_data = nutrition_response.json()
nutrition_data_exercises = nutrition_data["exercises"]

today_date = datetime.now().strftime("%d/%m/%Y")
time_now = datetime.now().strftime("%X")

for exercise in nutrition_data_exercises:
    sheety_header = {
        "Authorization": f"Bearer {SHEET_AUTHENTICATION}"
    }
    sheety_params = {
        "workout": {
            "date": today_date,
            "time": time_now,
            "exercise": exercise["user_input"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    sheety_response = requests.post(url=SHEET_ENDPOINT, json=sheety_params, headers=sheety_header)