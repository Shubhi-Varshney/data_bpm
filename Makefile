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

# run_train -s will train the model and pickle (save) it
run_train_cluster:
	python -c 'from data_bpm.interface.main import train; train(save_model=True if "-s" in "$(MAKEFLAGS)" else False)'
 	#python -c 'from data_bpm.interface.main import train; train()'

run_train_classification:
	python -c 'from data_bpm.interface.main import train_model2; train_model2(save=True)'


################### LOCAL REGISTRY ################

# Retrieve the user's home directory using Python
# HOME := $(shell python -c "from os.path import expanduser; print(expanduser('~'))")

# LOCAL_REGISTRY_PATH =  ~/.lewagon/data_bpm

# reset_local_files:
# 	rm -rf ${LOCAL_REGISTRY_PATH}
# 	mkdir -p ${LOCAL_REGISTRY_PATH}
# 	mkdir ${LOCAL_REGISTRY_PATH}/training_outputs
# 	mkdir ${LOCAL_REGISTRY_PATH}/training_outputs/models
# 	mkdir ${LOCAL_REGISTRY_PATH}/training_outputs/pipes


run_local_docker_image:
	docker run -e PORT=8000 -p 8080:8000 --env-file .env ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${DOCKER_REPO_NAME}/${DOCKER_IMAGE_NAME}:dev_13

build_docker_image:
	docker build -t ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${DOCKER_REPO_NAME}/${DOCKER_IMAGE_NAME}:dev_13 .

push_docker_image:
	docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${DOCKER_REPO_NAME}/${DOCKER_IMAGE_NAME}:dev_13

run_gcs_docker_image:
	gcloud run deploy --image ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${DOCKER_REPO_NAME}/${DOCKER_IMAGE_NAME}:dev_13 --region ${GCP_REGION} --env-vars-file .env.yaml

#LOCAL_REGISTRY_PATH =  ${HOME}/.lewagon/data_bpm
reset_local_files:
	rm -rf data_bpm/training_outputs
	mkdir -p data_bpm/training_outputs
	mkdir data_bpm/training_outputs/models
	mkdir data_bpm/training_outputs/pipes
