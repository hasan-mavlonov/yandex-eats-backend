FROM python:3.12
LABEL maintainer="yandex_eats_backend"
ENV PYTHONUNBUFFERED=1

ENV DB_NAME=yandex_eats_backend
ENV DB_USER=postgres
ENV DB_PASSWORD=saida0525
ENV DB_HOST=localhost
ENV DB_PORT=5432

# Create a new user and set as the default user
COPY ./requirements.txt /app/requirements.txt
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /app/requirements.txt && \
    adduser --disabled-password django-user && \
    chown -R django-user /app

# Copy the rest of the application code
COPY ./ /app
WORKDIR /app

# Set environment variables
USER django-user

ENV PATH="/venv/bin:$PATH"

# Expose the port that the app will run on
EXPOSE 8000

# Command to run the application with the virtual environment
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
