# Base Image
FROM python:3.10.5-slim-buster

# Working Directory
WORKDIR /usr/src/app

# Set Environment Variables

# :Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# :Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install System Dependencies
RUN apt update \
    && apt -y install netcat gcc \
    && apt clean \

# Install Python Dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .

# Cache Python Packages to the Docker Host: using the BuildKit: an opt-in image building engine which offers substantial improvements over the traditional process.
# new caching mechanism that can cache these dependencies download, instead of downloading them each time.
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

# Add app
COPY . .

# add entrypoint.sh
COPY entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]