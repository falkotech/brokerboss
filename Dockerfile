


FROM python:3.9-slim-bullseye AS base
WORKDIR /
RUN set -xe \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y mosquitto systemd
RUN pip install --upgrade pip
COPY ./requirements.txt /
RUN pip install -r /requirements.txt

# Create the mosquitto config and log directory and files
RUN mkdir -p /mosquitto/config
RUN echo "" > /mosquitto/config/pw.txt
RUN mkdir -p /mosquitto/log
RUN echo "" > /mosquitto/log/mosquitto.log
COPY ./mosquitto/mosquitto.service /etc/systemd/system/mosquitto.service
COPY ./log_config /log_config
# Copy the mosquitto configuration file to the container
COPY ./mosquitto/config/mosquitto.conf /mosquitto/config/mosquitto.conf
# Copy the mosquitto acl file to the container
COPY ./mosquitto/config/acl.acl /mosquitto/config/acl.acl
# Copy the tests to the container
COPY ./tests /tests
COPY ./run_app.py /
COPY ./app /app
EXPOSE 1883
EXPOSE 5000

CMD ["python3", "/run_app.py"]