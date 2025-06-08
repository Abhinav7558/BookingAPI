from datetime import datetime
import os
from dotenv import load_dotenv
import json

from app.database import SessionLocal
from app.models import FitnessClass
from app.utils.timezone_utils import convert_timezone_to_utc


load_dotenv()

CLASSES_FILE = os.environ.get('CLASSES_FILE')

with open(CLASSES_FILE) as file:
    classes_data = json.load(file)

def initial_data_load_fitness_classes():
    db = SessionLocal() 
    try:
        if db.query(FitnessClass).first():
            print("Data already inserted.")
            return

        for cls in classes_data:
            naive  = datetime.fromisoformat(cls["scheduled_at"])
            utc_dt = convert_timezone_to_utc(naive)

            fitness_class = FitnessClass(
                name=cls["name"],
                scheduled_at=utc_dt,
                instructor=cls["instructor"],
                total_slots=cls["slots"],
                available_slots=cls["slots"],
            )
            db.add(fitness_class)
            db.commit()
        print("Initial data inserted.")
    finally:
        db.close()
