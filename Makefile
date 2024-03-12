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

# run_pred:
# 	python -c 'from taxifare.interface.main import pred; pred()'


# run_all: run_preprocess run_train run_pred run_evaluate

# run_workflow:
# 	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m taxifare.interface.workflow

################### LOCAL REGISTRY ################

# Data sources: targets for monthly data imports

# Retrieve the user's home directory using Python
# HOME := $(shell python -c "from os.path import expanduser; print(expanduser('~'))")
#LOCAL_REGISTRY_PATH =  ${HOME}/.lewagon/data_bpm
reset_local_files:
	rm -rf data_bpm/training_outputs
	mkdir -p data_bpm/training_outputs
	mkdir data_bpm/training_outputs/models
	mkdir data_bpm/training_outputs/pipes
