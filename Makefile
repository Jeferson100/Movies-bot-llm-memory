install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

format:
	black chat_bots/*.py extracao/*.py funcoes_auxiliares/*.py tests/*.py app_streamlit.py

lint:
	pylint --disable=R,C chat_bots/*.py extracao/*.py funcoes_auxiliares/*.py tests/*.py app_streamlit.py

typepyright:
	pyright chat_bots/*.py extracao/*.py funcoes_auxiliares/*.py tests/*.py app_streamlit.py

typemypy:
	mypy chat_bots/ extracao/  funcoes_auxiliares/  tests/*.py app_streamlit.py

test:
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: install lint format test typepyright