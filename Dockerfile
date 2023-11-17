# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
COPY requirements.txt /
COPY src/ /src/

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# set our context
WORKDIR /src

# Run the script as a module
CMD ["python", "-m", "latency.write_to_gcs"]
