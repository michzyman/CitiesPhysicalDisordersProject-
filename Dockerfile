FROM python:3.6

WORKDIR /code

COPY . .

RUN pip install -r frontend/requirements.txt
RUN pip install -r parcel_info_collection/requirements.txt
RUN pip install -r google_maps_queries/requirements.txt

EXPOSE 5000

RUN ["chmod", "+x", "./start.sh"]
CMD ["./start.sh"]
