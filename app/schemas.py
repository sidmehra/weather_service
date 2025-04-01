# here we create the pydantic schema for data validation 
# validates the incoming json for POST /data
# it is also for documenting your API 

from pydantic import BaseModel, model_validator
from typing import Optional
from app.utils import validate_and_normalize_sensor_id, validate_metric_range

class WeatherDataCreate(BaseModel):
    sensor_id: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    windspeed: Optional[float] = None

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, values):
        sensor_id = values.get("sensor_id")
        temp = values.get("temperature")  # Pydantic will catch "abc", "20sd", @fsdf345 etc.
        humid = values.get("humidity")
        wind = values.get("windspeed")

        # validation logic for sensor id 
        sensor_id = validate_and_normalize_sensor_id(sensor_id)
        values["sensor_id"] = sensor_id

        # Ensure at least one metric is provided
        if all(v is None for v in [temp, humid, wind]):
            raise ValueError("At least one of temperature, humidity, or windspeed must be provided.")

        # Validate temperature
        if temp is not None:
            values["temperature"] = validate_metric_range("temperature", temp, -100, 100)

        # Validate humidity
        if humid is not None:
            values["humidity"] = validate_metric_range("humidity", humid, 0, 100)

        # Validate windspeed
        if wind is not None:
            values["windspeed"] = validate_metric_range("windspeed", wind, 0, 100)

        return values