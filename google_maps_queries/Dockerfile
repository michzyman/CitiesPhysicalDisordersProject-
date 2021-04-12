FROM python:3.6

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

RUN mkdir output output/OCCUPIED_STRUCTURE output/VACANT_LOT output/VACANT_STRUCTURE

ENTRYPOINT ["python"]

CMD ["google_satellite_view.py"]
