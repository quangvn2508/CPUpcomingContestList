env:
	python3 -m venv env

prep:
	source ./env/bin/activate
	pip install -r requirements.txt

run:
	source ./env/bin/activate
	python main.py