from OpenWeatherAPI import OpenWeatherAPI
from celery import Celery
from Utils import Utils
from time import sleep
from datetime import datetime

celery = Celery("Request")
celery.conf.broker_url = Utils.CELERY_BROKER_URL
celery.conf.result_backend = Utils.CELERY_RESULT_BACKEND
    
@celery.task(bind=True)
def new_request(self, userId: str) -> None:
    
    self.update_state(state="PROCESSING", meta={"progress": 0})
    
    api = OpenWeatherAPI()
    cities = Utils.CITY_IDS2
    time = datetime.now()
    data = {
        "userId": userId,
        "time": time,
        "weather": []
    }
    
    for idx, city in enumerate(cities):
        weather = api.get_current_weather(city)
        
        # In case city does not exist
        if(type(weather) == int and weather == 404):
            print(f"City with ID: {city} was not found. Skiping it.")
            continue
        elif(type(weather) == int and weather >= 500):
            print(f"Something is wrong with OpenWeather servers. Error returned: {weather}. Trying to skip this city")
            continue
            
        temperature = weather.get("main").get("temp")
        humidity = weather.get("main").get("humidity")
        data["weather"].append({
            "cityId": f"{city}",
            "temperature": temperature,
            "humidity": humidity
        })
        
        print({
            "cityId": f"{city}",
            "temperature": temperature,
            "humidity": humidity
        })
        
        self.update_state(state="PROCESSING", meta={"progress": ((idx+1)/len(cities))*100})
    
    self.update_state(state="PROCESSING", meta={"progress": 99})
    return {"result": "Task is done!", "progress": 100, "data": data}