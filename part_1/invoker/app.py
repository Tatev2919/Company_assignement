from flask import Flask, request, jsonify
from redis import Redis
import requests
from threading import Thread
import json
from time import time

app = Flask(__name__)
redis = Redis(host='redis', port=6379, db=0, decode_responses=True)
local_cache = {}
local_cache_ttl = {}

def fetch_recommendation(model_name, viewer_id):
    try:
        response = requests.post('http://generator:5000/generate', json={"model_name": model_name, "viewer_id": viewer_id}, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        app.logger.error(f"Error fetching recommendation: {e}")
        return {"reason": model_name, "result": "Error"}

def runcascade(viewer_id):
    model_names = ["model1", "model2", "model3", "model4", "model5"]
    threads = []
    results = []

    def worker(model_name):
        result = fetch_recommendation(model_name, viewer_id)
        results.append(result)

    for name in model_names:
        thread = Thread(target=worker, args=(name,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    viewer_id = data.get('viewer_id')
    if not viewer_id:
        return jsonify({"error": "Missing viewer_id"}), 400

    try:
        if viewer_id in local_cache and time() < local_cache_ttl[viewer_id] + 10:
            return jsonify(local_cache[viewer_id])
        
        cached_response = redis.get(viewer_id)
        if cached_response:
            return jsonify(json.loads(cached_response))

        results = runcascade(viewer_id)
        redis.set(viewer_id, json.dumps(results), ex=120)
        local_cache[viewer_id] = results
        local_cache_ttl[viewer_id] = time()
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

