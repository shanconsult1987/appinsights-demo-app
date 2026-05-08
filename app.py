from flask import Flask, jsonify, request
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
import os
import random
import time

# ----------------------------------------
# Flask App Initialization
# ----------------------------------------

app = Flask(__name__)

# ----------------------------------------
# Logging Configuration
# ----------------------------------------

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Prevent duplicate logs
if not logger.handlers:

    connection_string = os.environ.get(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )

    if connection_string:
        logger.addHandler(
            AzureLogHandler(
                connection_string=connection_string
            )
        )

# Startup Log
logger.warning("Application Started Successfully")

# ----------------------------------------
# Home Endpoint
# ----------------------------------------

@app.route("/")
def home():

    logger.info("Home endpoint called")

    return jsonify({
        "message": "Azure Application Insights Demo Running"
    })


# ----------------------------------------
# Slow API Endpoint
# Used for Profiler Demonstration
# ----------------------------------------

@app.route("/slow")
def slow():

    logger.info("Slow endpoint started")

    start = time.time()

    # Simulate slow processing
    time.sleep(5)

    duration = time.time() - start

    logger.warning(f"Slow API executed in {duration} seconds")

    return jsonify({
        "message": "Slow API completed",
        "duration_seconds": duration
    })


# ----------------------------------------
# Failure Endpoint
# Used for Exception Tracking Demo
# ----------------------------------------

@app.route("/fail")
def fail():

    logger.error("Failure endpoint triggered")

    try:
        x = 1 / 0
        return str(x)

    except Exception as e:

        logger.exception("Exception occurred in /fail endpoint")

        return jsonify({
            "error": str(e)
        }), 500


# ----------------------------------------
# Random Failure Endpoint
# Useful for Availability & Alert Demos
# ----------------------------------------

@app.route("/random")
def random_api():

    logger.info("Random endpoint called")

    if random.randint(1, 2) == 1:

        logger.error("Random failure generated")

        raise Exception("Random Failure Occurred")

    logger.info("Random endpoint succeeded")

    return jsonify({
        "message": "Random endpoint success"
    })


# ----------------------------------------
# Health Check Endpoint
# Useful for Ping Tests
# ----------------------------------------

@app.route("/health")
def health():

    logger.info("Health check endpoint called")

    return jsonify({
        "status": "healthy"
    })


# ----------------------------------------
# Request Telemetry Example
# ----------------------------------------

@app.route("/user/<username>")
def user(username):

    logger.info(f"User endpoint accessed for: {username}")

    return jsonify({
        "user": username
    })


# ----------------------------------------
# POST Request Example
# ----------------------------------------

@app.route("/submit", methods=["POST"])
def submit():

    data = request.json

    logger.info(f"POST payload received: {data}")

    return jsonify({
        "received_data": data
    })


# ----------------------------------------
# Main Entry Point
# ----------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )