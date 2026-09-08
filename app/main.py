import os
import time
from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['endpoint'])

items = [
    {"id": 1, "name": "Server 1", "status": "active"},
    {"id": 2, "name": "Database 1", "status": "active"}
]

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(request.path).observe(latency)
    REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    return response

@app.route('/')
def home():
    return jsonify({"status": "API is running"})

@app.route('/health')
def health():
    return jsonify({"status": "UP", "time": time.time()})

@app.route('/api/v1/items', methods=['GET', 'POST'])
def manage_items():
    if request.method == 'POST':
        data = request.json
        if not data or 'name' not in data:
            return jsonify({"error": "name is required"}), 400
        
        new_item = {
            "id": len(items) + 1,
            "name": data["name"],
            "status": data.get("status", "new")
        }
        items.append(new_item)
        return jsonify(new_item), 201
        
    return jsonify({"count": len(items), "data": items})

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    app.run(host='0.0.0.0', port=port)
