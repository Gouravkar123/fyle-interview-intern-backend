# Use the official Python image as a base
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=core/server.py

# Expose the port your app runs on
EXPOSE 7755

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=7755"]
