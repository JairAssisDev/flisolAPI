FROM python:3.11.6-slim-bookworm
LABEL authors = "JairAssisDev"
RUN pip install gunicorn

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
