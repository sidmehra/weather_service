from fastapi import HTTPException

def validate_and_normalize_sensor_id(sensor_id: str) -> str:
    """
    Validates that the sensor_id is a numeric string between 1 and 50.
    Returns the normalized (cleaned) string version of the sensor_id.
    Raises HTTPException if invalid.
    """
    if not sensor_id or not sensor_id.strip().isdigit():
        raise HTTPException(status_code=400, detail="Sensor ID must be a numeric string.")

    sensor_id_int = int(sensor_id.strip())
    if not (1 <= sensor_id_int <= 50):
        raise HTTPException(status_code=400, detail="Sensor ID must be between 1 and 50.")

    return str(sensor_id_int)

def validate_metric_range(metric_name: str, value: float, min_value: float, max_value: float) -> float:
    if not (min_value <= value <= max_value):
        raise ValueError(f"{metric_name.capitalize()} must be between {min_value} and {max_value}.")
    return value
