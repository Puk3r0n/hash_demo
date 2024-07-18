dependencies: dependencies

# Target to install dependencies
dependencies:
	python3 -m pip install -r requirements.txt

setup: start lint

# Target to run project
start:
	 python main.py

# Target to run pylint
lint:
	 pylint src

test: test

test:
	PYTHONPATH=$$PYTHONPATH:$(pwd) pytest tests
