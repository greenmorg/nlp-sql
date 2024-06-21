FROM python:3.11-slim
WORKDIR /src
COPY . .
RUN apt-get update && apt upgrade -y
# run the setup.py for db setup from another container
RUN pip install -r requirements.txt