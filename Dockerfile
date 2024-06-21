FROM python:3.11-slim
WORKDIR /app
COPY . /app/
RUN apt-get update && apt upgrade -y
ENV PYTHONPATH=/app/
# run the setup.py for db setup from another container
RUN pip install -r ./src/requirements.txt