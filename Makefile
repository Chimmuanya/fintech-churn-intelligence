.PHONY: venv install gen preprocess notebook dashboard

install:
	python3 -m pip install --upgrade pip
	pip install -r requirements.txt

gen:
	python scripts/generate_synthetic_events.py

preprocess:
	python scripts/preprocess.py

notebook:
	jupyter lab

dashboard:
	streamlit run dashboard/app.py
