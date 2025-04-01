# here we define our database table structure 

from sqlalchemy import Column, Integer, Float, String, DateTime
from app.database import Base
from datetime import datetime

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    windspeed = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
