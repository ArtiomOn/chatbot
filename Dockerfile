# Use the Python 3.12 base image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY . /app/

# Run collectstatic to gather static files
RUN python manage.py collectstatic --noinput

# Apply database migrations
RUN python manage.py migrate --noinput

# Expose the port your app will run on
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
