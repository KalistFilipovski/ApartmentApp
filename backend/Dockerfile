# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements files
COPY requirements.txt requirements.txt

# Install the backend and frontend dependencies
RUN pip install -r requirements.txt 

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
EXPOSE 3000

# Run the application
CMD ["python", "main.py"]
