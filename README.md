# Project diagram
[![Diagram.png](https://i.postimg.cc/zBr2xqMr/Diagram.png)](https://postimg.cc/t1BzTGpS)
# How to use this project
1. Create a .env file in the root folder containing the following contents:
`API_KEY="<YourOpenWeatherApiKeyHere>"`

2. Run the following command to build the docker images and start the containers:
`docker compose up --build`

3. On the command prompt, use cURL or equivalent to send a POST request to the API (depending on your OS, you may need to escape the double-quotes in the json payload):
`curl -i -X POST -H "Content-Type: application/json" -d "{"userId":"<userId>"}" http://localhost:8000/`

4. Track user requests progress on `http://localhost:8000/<userId>`

5. For testing, please run the following command and wait until it finishes: `docker exec frontend coverage run -m unittest discover -s tests`

6. Review the test coverage: `docker exec frontend coverage report`
# Test Coverage
[![Test-Coverage.png](https://i.postimg.cc/TYxVt17w/Test-Coverage.png)](https://postimg.cc/F1PkRrQ5)

# Resources used
### requests - https://pypi.org/project/requests/
Used to make HTTP requests in a simpler way.
### fastapi - https://fastapi.tiangolo.com/
Used as a web framework to develop APIs. The usage of this framework makes it easier to create endpoint routes.
### python-dotenv - https://pypi.org/project/python-dotenv/
Used to restore environment variables, as sensistive information, such as the api_key, are stored there rather than hardcoded.
### celery - https://docs.celeryq.dev/en/stable/index.html
This is used to handle asynchronous tasks and background jobs, allowing the application to perform long-running operations without blocking the main process. This way, users can still make new requests to the API without the need to wait synchronously the answer.
### uvicorn - https://www.uvicorn.org/
This is an ASGI (Asynchronous Server Gateway Interface) server used to run the main Python web server.
### httpx - https://www.python-httpx.org/
This library is needed to run the unit test modules.
### coverage - https://coverage.readthedocs.io/en/7.6.1/
This library is used to run the unit tests and to calculate the coverage percentage of unit tests in this application.