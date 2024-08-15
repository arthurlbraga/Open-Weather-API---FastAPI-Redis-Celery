from dotenv import dotenv_values
from Utils import Utils
import json
import requests
from time import sleep

class OpenWeatherAPI:
    def __init__(self) -> None:
        config = dotenv_values(".env")
        self.api_key = config.get('API_KEY')
        self.base_url = f'{Utils.OW_BASE_URL}?appid={self.api_key}'
    
    # Endpoint info at: https://openweathermap.org/current#cityid
    def get_current_weather(self, id: int) -> json:        
        # Check possible returns at: https://openweathermap.org/faq
        success = False
        while(not success):
            r = requests.get(f'{self.base_url}&id={id}&units={Utils.BASE_UNIT}')
            print(f'{self.base_url}&id={id}&units={Utils.BASE_UNIT} --- {r.status_code}')
            
            if(r.status_code == 200): # Success
                success = True
            elif(r.status_code == 429): # Rate Limit
                print("ERROR: Rate limit. Trying again in 10 seconds")
                print(r.json())
                sleep(10)
            elif(r.status_code == 404): # City not found
                break
            elif(r.status_code >= 500): # Error in OpenWeather servers
                break
            else:
                print(r.json())
        
        if(r.status_code == 200):
            response = r.json()
        elif(r.status_code == 404 or r.status_code >= 500):
            response = r.status_code
            
        return response