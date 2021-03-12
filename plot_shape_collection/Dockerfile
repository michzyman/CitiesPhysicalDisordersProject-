FROM joyzoursky/python-chromedriver:3.6

WORKDIR /project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENTRYPOINT ["python", "plot_shape_collection.py"]
