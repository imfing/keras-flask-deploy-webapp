FROM python:3.11-slim-buster

# Install dependencies
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

COPY . /app
WORKDIR /app

# Run the application on port 5000
EXPOSE 5000
CMD ["python", "app.py"]
