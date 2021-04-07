FROM python:3.6

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENTRYPOINT ["python"]

CMD ["parcel_info_collection.py"]
