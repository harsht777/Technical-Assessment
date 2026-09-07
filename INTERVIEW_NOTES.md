# My Interview Notes

Here are some notes I put together to help me explain my project during the interview.

## How it works (Simple Version)
- **Nginx** is like the front door. It receives the request on port 80 and passes it to the API.
- The **Flask API** does the actual work. It handles the routes like `/health` and `/api/v1/items`.
- **Prometheus** checks the `/metrics` endpoint every 5 seconds to collect data (like how many requests came in).
- **Grafana** reads that data from Prometheus and shows it in nice graphs.
- **Jenkins** automates testing and running the Docker containers so I don't have to type the commands manually.

## Why did I use Nginx?
I used Nginx as a reverse proxy because Flask's built-in server isn't meant for production. Nginx can handle lots of connections safely and it hides the backend API port (5000) from the outside world.

## How do the metrics work?
I used the `prometheus_client` library in Python.
- **Counter**: I used this to count the total number of HTTP requests. It only goes up.
- **Histogram**: I used this to measure how long requests take (latency).

Every time a request comes in, my `@app.after_request` function updates these metrics.

## What's in the Dockerfile?
I started with `python:3.10-slim` to keep the image small. Then I copied my `requirements.txt` and ran `pip install`. After that, I copied the rest of the app and told it to run `app/main.py`.

## What does the Jenkinsfile do?
It's a simple pipeline with these steps:
1. **Checkout**: Pull the code.
2. **Build**: Install python dependencies.
3. **Test**: Run my `pytest` tests.
4. **Docker Build**: Build the Docker image.
5. **Deploy**: Run `docker compose up -d` to start the containers.
6. **Health Check**: Run a `curl` command to make sure the `/health` endpoint is returning a response.

## What alerts did I set up?
In `alert.rules.yml`, I set up rules so Prometheus will know if something goes wrong:
- **APIDown**: Triggers if Prometheus can't reach the API for 30 seconds.
- **HighErrorRate**: Triggers if too many requests start failing with 5xx errors.
- **HighLatency**: Triggers if requests are taking too long to respond.
