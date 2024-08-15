from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from Worker import Worker
import uvicorn

app = FastAPI()
tasks = {}
worker = Worker()


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("./static/pollo.ico")

@app.get("/")
async def index():
    return {"INFO": "You can use this API by sending a POST request containing the following body: {'userId': '<userID>'}. Additionally you can track requests for created users by sending a GET request to /<userID>"}

@app.post("/")
async def new_user(data=Body(...)):   
    if("userId" not in data):
        return {"ERROR": "No userId provided in the payload"}
    
    userId = str(data["userId"])
    if(userId not in tasks):
        if("testing" in data):
            task = worker.new_request.delay(userId, True)
        else:
            task = worker.new_request.delay(userId, False)
        
        tasks[userId] = task.id
        return {"INFO": f"New request created with TaskID = {task.id}"}
    else:
        return {"INFO": "A request was already created for this User ID"}

@app.get("/{userId}" )
async def check_user(userId: str):
    if(userId in tasks):
        task = worker.new_request.AsyncResult(tasks[userId])
        if(int(task.info.get("progress", 0)) < 100):
            return {"INFO": f"The request for this user is being processed. Status = {int(task.info.get("progress", 0))}%"}
        else:
            return {"INFO": f"The request for this user has been completed. Status = {int(task.info.get("progress", 0))}%", "data": task.info.get("data", 0) }
    else:
        return {"ERROR": "The User ID informed doesn't exist in our database"}