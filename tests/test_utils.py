from app.utils import validate_and_normalize_sensor_id
from app.utils import validate_metric_range
import pytest

def test_valid_sensor_id():
    assert validate_and_normalize_sensor_id("5") == "5"

def test_invalid_sensor_id_non_numeric():
    with pytest.raises(Exception):
        validate_and_normalize_sensor_id("abc") # invalid: letters 

def test_invalid_sensor_id_out_of_range():
    with pytest.raises(Exception):
        validate_and_normalize_sensor_id("99") # invalid: above valid range 

def test_invalid_sensor_id_less_than_one():
    with pytest.raises(Exception):
        validate_and_normalize_sensor_id("0")  # invalid: below valid range

def test_invalid_sensor_id_alphanumeric():
    with pytest.raises(Exception):
        validate_and_normalize_sensor_id("5A")  # invalid: letters + numbers

def test_invalid_sensor_id_special_characters():
    with pytest.raises(Exception):
        validate_and_normalize_sensor_id("@3")  # invalid: special characters


def test_validate_metric_range_valid():
    assert validate_metric_range("temperature", 25.0, -100, 100) == 25.0

def test_validate_metric_range_min_boundary():
    assert validate_metric_range("humidity", 0, 0, 100) == 0

def test_validate_metric_range_max_boundary():
    assert validate_metric_range("humidity", 100, 0, 100) == 100

def test_validate_metric_range_below_min():
    with pytest.raises(ValueError) as exc:
        validate_metric_range("windspeed", -1, 0, 100)
    assert "Windspeed must be between 0 and 100." in str(exc.value)

def test_validate_metric_range_above_max():
    with pytest.raises(ValueError) as exc:
        validate_metric_range("temperature", 120, -100, 100)
    assert "Temperature must be between -100 and 100." in str(exc.value)
