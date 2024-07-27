  
FROM python:3.9

RUN mkdir -p /fastapi-app
WORKDIR /fastapi-app

# Copy files
COPY ./requirements.txt ./

# Copy folders
COPY ./app ./app

# Install packages
RUN pip install -r requirements.txt
