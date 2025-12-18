# Use an official lightweight Python image.
FROM python:latest

# Set the working directory in the container.
WORKDIR /app

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container.
COPY . .

# Expose the port the app runs on.
EXPOSE 8080

# Make the entrypoint script executable.
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script.
ENTRYPOINT ["/app/entrypoint.sh"]
