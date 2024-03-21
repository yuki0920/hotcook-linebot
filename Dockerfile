# Dockerfile
FROM python:3.11

RUN apt-get update -y && \
	apt install -y wget make

RUN curl -sSL https://install.python-poetry.org | python3 -
# Path for poetry
ENV PATH /root/.local/bin/:$PATH

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main

COPY . .

EXPOSE 8080

# Run the application without poetry for production
CMD ["python", "hotcook-linebot/main.py"]
