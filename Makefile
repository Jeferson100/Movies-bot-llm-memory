install:
	uv pip install --upgrade pip && \
		uv pip install -r requirements.txt

format:
	black chat_bots/*.py extracao/*.py funcoes_auxiliares/*.py app_streamlit.py

lint:
	pylint --disable=R,C chat_bots/*.py extracao/*.py funcoes_auxiliares/*.py app_streamlit.py

typepyright:
	pyright chat_bots/*.py extracao/*.py funcoes_auxiliares/*.py app_streamlit.py

typemypy:
	mypy chat_bots/*.py extracao/*.py funcoes_auxiliares/*.py app_streamlit.py

test:
	python -m pytest -vv --cov=tests/test_*.py

refactor: format lint

all: install lint format test