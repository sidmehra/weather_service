from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app import database, models
from enum import Enum
from app.utils import validate_and_normalize_sensor_id

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Statistic(str, Enum):
    min = "min"
    max = "max"
    sum = "sum"
    average = "average"

class Metric(str, Enum):
    temperature = "temperature"
    humidity = "humidity"
    windspeed = "windspeed"

@router.get("/query")
def query_sensor_data(
    sensor_id: str,
    metrics: list[Metric] = Query(..., description="Select one or more metrics"),
    statistics: list[Statistic] = Query(..., description="Select one of more statistics to calculate"),
    days: int = Query(None, ge=1, le=30),
    db: Session = Depends(get_db)
):
    
    # Validate and normalize sensor_id
    sensor_id = validate_and_normalize_sensor_id(sensor_id)
    results = {}

    for metric_enum in metrics:
        metric = metric_enum.value
        metric_column = getattr(models.WeatherData, metric, None)
        if metric_column is None:
            continue

        metric_results = {}

        for stat_enum in statistics:
            stat = stat_enum.value
            query = db.query(metric_column)

            # Apply statistic function
            if stat == "min":
                query = db.query(func.min(metric_column))
            elif stat == "max":
                query = db.query(func.max(metric_column))
            elif stat == "sum":
                query = db.query(func.sum(metric_column))
            elif stat == "average":
                query = db.query(func.avg(metric_column))

            # Filter by sensor and date
            query = query.filter(models.WeatherData.sensor_id == sensor_id)

            if days:
                start_time = datetime.utcnow() - timedelta(days=days)
                query = query.filter(models.WeatherData.timestamp >= start_time)
            else:
                latest_entry = (
                    db.query(models.WeatherData)
                    .filter(models.WeatherData.sensor_id == sensor_id)
                    .order_by(models.WeatherData.timestamp.desc())
                    .first()
                )
                metric_results[stat] = getattr(latest_entry, metric) if latest_entry else None
                continue

            value = query.scalar()
            metric_results[stat] = round(value, 2) if value is not None else None

        results[metric] = metric_results

    return {
        "sensor_id": sensor_id,
        "days": days,
        "results": results
    }