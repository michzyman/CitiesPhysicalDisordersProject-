FROM python:3.6

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 8080

CMD ["gunicorn", "-b", ":8080", "app:app"]
