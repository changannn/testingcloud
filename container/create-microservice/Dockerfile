# Use the official Python runtime as a parent image
FROM python:3.12.0-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies required for building python mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8003 available to the world outside this container
EXPOSE 8003

# Define environment variable
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8003", "cloudproj.wsgi:application"]
