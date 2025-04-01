# seed_data.py

from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models import WeatherData
import random

db = SessionLocal()

# Clear existing records (optional for testing)
# db.query(WeatherData).delete()
# db.commit()

sensor_ids = [str(i) for i in range(1, 6)]  # "1" to "5"

now = datetime.utcnow()
used_timestamps = set()

for _ in range(100):
    sensor_id = random.choice(sensor_ids)

    # Generate a unique timestamp by adding seconds to a base datetime
    while True:
        random_days = random.randint(0, 29)
        random_seconds = random.randint(0, 86400)
        timestamp = now - timedelta(days=random_days, seconds=random_seconds)
        if timestamp not in used_timestamps:
            used_timestamps.add(timestamp)
            break

    entry = WeatherData(
        sensor_id=sensor_id,
        temperature=round(random.uniform(-50.0, 60.0), 1),
        humidity=round(random.uniform(0.0, 100.0), 1),
        windspeed=round(random.uniform(0.0, 100.0), 1),
        timestamp=timestamp
    )
    db.add(entry)

db.commit()
db.close()

print("Successfully seeded 100 realistic sensor entries.")
