FROM python:3.10.6-buster

COPY requirements_prod.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY raw_data /raw_data
COPY data_bpm /data_bpm
COPY setup.py setup.py

RUN pip install .

COPY nltk_data /usr/share/nltk_data

COPY Makefile Makefile
RUN make run_preprocess
RUN make run_train_classification

CMD uvicorn data_bpm.api.bpm:app --host 0.0.0.0 --port $PORT
