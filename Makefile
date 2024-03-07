.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
reinstall_package:
	@pip uninstall -y data_bpm || :
	@pip install -e .

run_preprocess:
	python -c 'from data_bpm.interface.main import preprocess; preprocess()'


clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr data_bpm-*.dist-info
	@rm -fr data_bpm.egg-info

# run_train:
# 	python -c 'from taxifare.interface.main import train; train()'

# run_pred:
# 	python -c 'from taxifare.interface.main import pred; pred()'

# run_evaluate:
# 	python -c 'from taxifare.interface.main import evaluate; evaluate()'

# run_all: run_preprocess run_train run_pred run_evaluate

# run_workflow:
# 	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m taxifare.interface.workflow

##################### TESTS #####################

################### DATA SOURCES ACTIONS ################

# Data sources: targets for monthly data imports
# ML_DIR=~/.lewagon/mlops
# HTTPS_DIR=https://storage.googleapis.com/datascience-mlops/taxi-fare-ny/
# GS_DIR=gs://datascience-mlops/taxi-fare-ny

# show_sources_all:
# 	-ls -laR ~/.lewagon/mlops/data
# 	-bq ls ${BQ_DATASET}
# 	-bq show ${BQ_DATASET}.processed_1k
# 	-bq show ${BQ_DATASET}.processed_200k
# 	-bq show ${BQ_DATASET}.processed_all
# 	-gsutil ls gs://${BUCKET_NAME}

# reset_local_files:
# 	rm -rf ${ML_DIR}
# 	mkdir -p ~/.lewagon/mlops/data/
# 	mkdir ~/.lewagon/mlops/data/raw
# 	mkdir ~/.lewagon/mlops/data/processed
# 	mkdir ~/.lewagon/mlops/training_outputs
# 	mkdir ~/.lewagon/mlops/training_outputs/metrics
# 	mkdir ~/.lewagon/mlops/training_outputs/models
# 	mkdir ~/.lewagon/mlops/training_outputs/params

# reset_local_files_with_csv_solutions: reset_local_files
# 	-curl ${HTTPS_DIR}solutions/data_query_fixture_2009-01-01_2015-01-01_1k.csv > ${ML_DIR}/data/raw/query_2009-01-01_2015-01-01_1k.csv
# 	-curl ${HTTPS_DIR}solutions/data_query_fixture_2009-01-01_2015-01-01_200k.csv > ${ML_DIR}/data/raw/query_2009-01-01_2015-01-01_200k.csv
# 	-curl ${HTTPS_DIR}solutions/data_query_fixture_2009-01-01_2015-01-01_all.csv > ${ML_DIR}/data/raw/query_2009-01-01_2015-01-01_all.csv
# 	-curl ${HTTPS_DIR}solutions/data_processed_fixture_2009-01-01_2015-01-01_1k.csv > ${ML_DIR}/data/processed/processed_2009-01-01_2015-01-01_1k.csv
# 	-curl ${HTTPS_DIR}solutions/data_processed_fixture_2009-01-01_2015-01-01_200k.csv > ${ML_DIR}/data/processed/processed_2009-01-01_2015-01-01_200k.csv
# 	-curl ${HTTPS_DIR}solutions/data_processed_fixture_2009-01-01_2015-01-01_all.csv > ${ML_DIR}/data/processed/processed_2009-01-01_2015-01-01_all.csv

reset_bq_files:
	-bq rm --project_id ${GCP_PROJECT} ${BQ_DATASET}.processed_1k
	-bq rm --project_id ${GCP_PROJECT} ${BQ_DATASET}.processed_200k
	-bq rm --project_id ${GCP_PROJECT} ${BQ_DATASET}.processed_all
	-bq mk --sync --project_id ${GCP_PROJECT} --location=${BQ_REGION} ${BQ_DATASET}.processed_1k
	-bq mk --sync --project_id ${GCP_PROJECT} --location=${BQ_REGION} ${BQ_DATASET}.processed_200k
	-bq mk --sync --project_id ${GCP_PROJECT} --location=${BQ_REGION} ${BQ_DATASET}.processed_all

reset_gcs_files:
	-gsutil rm -r gs://${BUCKET_NAME}
	-gsutil mb -p ${GCP_PROJECT} -l ${GCP_REGION} gs://${BUCKET_NAME}

reset_all_files: reset_local_files reset_bq_files reset_gcs_files
