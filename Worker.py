from OpenWeatherAPI import OpenWeatherAPI
from celery import Celery, Task
from Utils import Utils
from datetime import datetime

celery = Celery("Request")
celery.conf.broker_url = Utils.CELERY_BROKER_URL
celery.conf.result_backend = Utils.CELERY_RESULT_BACKEND
    
class Worker(Task):
        
    @celery.task(bind=True)
    def new_request(self, userId: str, testing: bool = False) -> None:
        
        if(not testing):
            self.update_state(state="PROCESSING", meta={"progress": 0})
        
        api = OpenWeatherAPI()
        cities = Utils.CITY_IDS
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
            
            if(not testing):
                self.update_state(state="PROCESSING", meta={"progress": ((idx+1)/len(cities))*100})
        
        if(not testing):
            self.update_state(state="PROCESSING", meta={"progress": 99})
        
        return {"result": "Task is done!", "progress": 100, "data": data}