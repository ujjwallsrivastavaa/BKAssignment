# Use an official Python runtime as the base image
FROM python:3.10-slim


# Set the working directory inside the container
WORKDIR /app

# Copy the current directory content into the container at /app
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Django runs on (default: 8000)
EXPOSE 8000

# Set environment variables for Django settings
ENV PYTHONUNBUFFERED 1

# Run the Django development server
CMD ["python", "server/manage.py", "runserver", "0.0.0.0:8000"]
