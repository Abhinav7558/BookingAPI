from datetime import datetime
import os
from dotenv import load_dotenv
import json

from app.database import SessionLocal
from app.models import FitnessClass


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
            scheduled_at = datetime.fromisoformat(cls["scheduled_at"])
            fitness_class = FitnessClass(
                name=cls["name"],
                scheduled_at=scheduled_at,
                instructor=cls["instructor"],
                total_slots=cls["slots"],
                available_slots=cls["slots"],
            )
            db.add(fitness_class)
            db.commit()
        print("Initial data inserted.")
    finally:
        db.close()
