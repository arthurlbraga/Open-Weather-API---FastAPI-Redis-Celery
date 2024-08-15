from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from celery_worker import new_request
import uvicorn
from OpenWeatherAPI import OpenWeatherAPI
from Utils import Utils
from time import sleep
from datetime import datetime



app = FastAPI()
tasks = {}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("./static/pollo.ico")

# This function is only for test purposes
# def test(userId):
#     api = OpenWeatherAPI()
#     cities = Utils.CITY_IDS
#     time = datetime.now()
#     data = {
#         "userId": userId,
#         "time": time,
#         "weather": []
#     }
    
#     for idx, city in enumerate(cities):
#         weather = api.get_current_weather(city)
#         temperature = weather.get("main").get("temp")
#         humidity = weather.get("main").get("humidity")
#         data["weather"].append({
#             "cityId": f"{city}",
#             "temperature": temperature,
#             "humidity": humidity
#         })

@app.get("/")
async def index():
    return {"INFO": "You can use this API by sending a POST request containing the following body: {'userId': '<userID>'}. Additionally you can track requests for created users by sending a GET request to /<userID>"}

@app.post("/")
async def new_user(data=Body(...)):
    userId = str(data["userId"])
    if(userId not in tasks):
        for i in range(10):
            userId = userId + str(i)
            task = new_request.delay(userId)
            tasks[userId] = task.id
        return {"INFO": f"New request created with TaskID = {task.id}"}
    else:
        return {"INFO": "A request was already created for this User ID"}

@app.get("/{userId}" )
async def check_user(userId: str):
    if(userId in tasks):
        task = new_request.AsyncResult(tasks[userId])
        if(int(task.info.get("progress", 0)) < 100):
            return {"INFO": f"The request for this user is being processed. Status = {int(task.info.get("progress", 0))}%"}
        else:
            return {"INFO": f"The request for this user has been completed. Status = {int(task.info.get("progress", 0))}%", "data": task.info.get("data", 0) }
    else:
        return {"ERROR": "The User ID informed doesn't exist in our database"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)