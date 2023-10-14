# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory within the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose ports used by the Flask apps
EXPOSE 5001
EXPOSE 5002
EXPOSE 5003

# Run the Python script that starts the Flask apps
CMD ["python", "app.py"]
