# Inspiration from: https://www.cloudbees.com/blog/monitoring-your-synchronous-python-web-applications-using-prometheus

from functools import wraps

from flask import request, current_app
import time
import prometheus_client as prom


# Setup Metrics you want to monitor
REQUEST_COUNT = prom.Counter(
    'request_count', 'App Request Count by status code, method and paths',
    ['app_name', 'method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = prom.Histogram('request_latency_seconds', 'Request latency',
                                 ['app_name', 'endpoint']
                                 )

KEY_COUNT = prom.Gauge(
    'server_key_count', 'Number of keys currently stored on server.')


# Method to monitor latency
def monitor_response_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        req_start_time = time.time()

        function_response = func(*args, **kwargs)

        resp_time = time.time() - req_start_time
        print(f"Took: {resp_time}")
        REQUEST_LATENCY.labels(
            current_app.name, request.path).observe(resp_time)
        return function_response
    return wrapper

# Method to monitor request
def monitor_status_code(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        function_response = func(*args, **kwargs)

        REQUEST_COUNT.labels(current_app.name, request.method, request.path,
                             function_response[1]).inc()

        return function_response
    return wrapper

# Method to show key count
def monitor_stored_keys(keys):
    print(len(keys))
    return KEY_COUNT.set(len(keys))
