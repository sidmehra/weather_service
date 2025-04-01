from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas, database
from app.utils import validate_and_normalize_sensor_id

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/data")
def create_weather_data(data: schemas.WeatherDataCreate, db: Session = Depends(get_db)):
    try:
        new_entry = models.WeatherData(**data.dict())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return {"message": "Data added successfully", "id": new_entry.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add data: {str(e)}")
    
@router.get("/data")
def get_all_data(db: Session = Depends(get_db)):
    records = db.query(models.WeatherData).all()

    if not records:
        return {"message": "No entries found in the database."}

    return {
        "message": f"Found {len(records)} entries in the database.",
        "data": records
    }

# @router.delete("/data")
# def delete_sensor_data(
#     sensor_id: str = Query(None, description="Optional sensor ID to delete specific sensor's data (1-50)"),
#     db: Session = Depends(get_db)
# ):
#     # Validate and normalize sensor_id if provided
#     if sensor_id:
#         sensor_id = validate_and_normalize_sensor_id(sensor_id)

#     # Build delete query
#     query = db.query(models.WeatherData)
#     if sensor_id:
#         query = query.filter(models.WeatherData.sensor_id == sensor_id)

#     count = query.count()

#     if count == 0:
#         if sensor_id:
#             return {"message": f"No records found for sensor '{sensor_id}'."}
#         else:
#             return {"message": "No records found in the database."}

#     query.delete(synchronize_session=False)
#     db.commit()

#     if sensor_id:
#         return {"message": f"Deleted {count} record(s) for sensor '{sensor_id}'."}
#     else:
#         return {"message": f"Deleted {count} record(s) (all sensors)."}
