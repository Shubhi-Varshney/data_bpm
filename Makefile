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
run_train:
	python -c 'from data_bpm.interface.main import train; train(save_model=True if "-s" in "$(MAKEFLAGS)" else False)'
 	#python -c 'from data_bpm.interface.main import train; train()'

# run_pred:
# 	python -c 'from taxifare.interface.main import pred; pred()'


# run_all: run_preprocess run_train run_pred run_evaluate

# run_workflow:
# 	PREFECT__LOGGING__LEVEL=${PREFECT_LOG_LEVEL} python -m taxifare.interface.workflow

################### LOCAL REGISTRY ################

# Data sources: targets for monthly data imports
LOCAL_REGISTRY_PATH =  ~/.lewagon/data_bpm

reset_local_files:
	rm -rf ${LOCAL_REGISTRY_PATH}
	mkdir -p ${LOCAL_REGISTRY_PATH}
	mkdir ${LOCAL_REGISTRY_PATH}/training_outputs
	mkdir ${LOCAL_REGISTRY_PATH}/training_outputs/models
