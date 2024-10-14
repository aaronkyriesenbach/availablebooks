FROM python:3.13.0

USER root

RUN apt-get update && apt-get install chromium-driver -y

RUN adduser reader

USER reader
WORKDIR /home/reader

RUN mkdir availablebooks
COPY main.py availablebooks/
COPY constants.py availablebooks/
COPY models availablebooks/models
COPY requirements.txt availablebooks/

WORKDIR availablebooks

RUN pip install -r requirements.txt

CMD ["python", "main.py"]