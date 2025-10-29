import json
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class Result(Generic[T]):
    def __init__(self, success: bool, data: Optional[T] = None, error: Optional[str] = None):
        self.success = success
        self.data = data
        self.error = error
        
    def __str__(self):
        return json.dumps({
            "success": self.success,
            "data": self.data.to_dict() if self.data else None,
            "error": self.error
        })

class Weather:
    def __init__(self, location, temp_celsius, humidity, condition, description):
        self.location = location
        self.temp_celsius = temp_celsius
        self.humidity = humidity
        self.condition = condition
        self.description = description
        
    def to_dict(self):
        return {
            "location": self.location,
            "temp_celsius": self.temp_celsius,
            "humidity": self.humidity,
            "condition": self.condition,
            "description": self.description,
        }
        
    def __str__(self):
        return json.dumps(self.to_dict())
    
class Event:
    def __init__(self, name, date, time, location, details):
        self.name = name
        self.date = date
        self.time = time
        self.location = location
        self.details = details
        
    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "time": self.time,
            "location": self.location,
            "details": self.details
        }
        
    def __str__(self):
        return json.dumps(self.to_dict())
    
class ListJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super().default(obj)