# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Make port 1235 available to the world outside this container
EXPOSE 1235

# Run app.py when the container launches
CMD ["uvicorn", "webserver:app", "--host", "0.0.0.0", "--port", "1235"]

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app
