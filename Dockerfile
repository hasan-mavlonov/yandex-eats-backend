FROM python:3.12
LABEL maintainer="yandex_eats_backend"
ENV PYTHONUNBUFFERED=1

# Set work directory and create a non-root user
WORKDIR /app
RUN adduser --disabled-password django-user

# Install dependencies (optimized for caching)
COPY ./requirements.txt /app/requirements.txt
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /app/requirements.txt

# Copy the rest of the application code and adjust ownership
COPY ./ /app
RUN chown -R django-user /app

# Switch to non-root user
USER django-user

# Set the virtual environment path
ENV PATH="/venv/bin:$PATH"

# Expose the default port
EXPOSE 8000

CMD ["/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
