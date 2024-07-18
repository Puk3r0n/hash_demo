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

tests: tests

# Target to run tests
tests:
	pytest tests/test.py
