# Pull base image
FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /code/entrypoint.sh

RUN chmod +x /code/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/code/entrypoint.sh"]