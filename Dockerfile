# Pull offical base image
FROM python:3.9-slim

# Set a work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONNUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8080" ]
