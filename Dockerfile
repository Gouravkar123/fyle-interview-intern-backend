# Use the official Python image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the current project into the container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port the application runs on
EXPOSE 5000

# Default command to run the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
