FROM python:3.8.12-buster

COPY requirements_prod.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY raw_data /raw_data
COPY data_bpm /data_bpm
COPY setup.py setup.py

RUN pip install .

COPY nltk_data /usr/share/nltk_data

COPY Makefile Makefile
RUN make reset_local_files

CMD uvicorn data_bpm.api.bpm:app --host 0.0.0.0 --port $PORT
