# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory within the container
WORKDIR /app/secondary1

# Copy the current directory contents into the container at /app
COPY . /app/secondary1

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose ports used by the Flask apps
EXPOSE 5000

# Run the Python script that starts the Flask apps
ENTRYPOINT ["python"]

CMD ["app_secondary1.py"]
