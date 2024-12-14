FROM python:3.12

# Create a new user and set as the default user
RUN useradd -m django_user
USER django_user

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create and activate the virtual environment inside the working directory
RUN python -m venv /app/venv
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

# Set environment variables
ENV PYTHONPATH=/app

# Expose the port that the app will run on
EXPOSE 8000

# Set the user back to django_user
USER django_user

# Command to run the application with the virtual environment
CMD ["/app/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
