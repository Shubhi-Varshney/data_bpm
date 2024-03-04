# 1> TO-DO decide local environment (from arguement)
# 2> Figure about global environments (PORT)

FROM 

COPY requirements.text requirements.txt
RUN pip install -r requirements.txt

COPY bpm /bpm
COPY setup.py setup.py
RUN pip install .

COPY Makefile Makefile
RUN make reset_local_files

CMD uvicorn bpm.api.bpm:app --host 0.0.0.0 --port $PORT