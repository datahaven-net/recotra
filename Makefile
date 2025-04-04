# This Makefile requires the following commands to be available:
# * virtualenv
# * python3.10

REQUIREMENTS_TXT:=requirements.txt

PIP:="venv/bin/pip"
PYTHON="venv/bin/python"
PYTHON_VERSION=python3.10

.PHONY: clean pyclean

pyclean:
	@find . -name *.pyc -delete
	@rm -rf *.egg-info build
	@rm -rf coverage.xml .coverage

clean: pyclean
	@rm -rf venv
	@rm -rf .tox

venv:
	@rm -rf venv
	@$(PYTHON_VERSION) -m venv venv
	@$(PIP) install --upgrade pip
	@$(PIP) install pgen==0.2.1
	@$(PIP) install Cython==3.0.0
	@$(PIP) install -r $(REQUIREMENTS_TXT)

pip_install:
	@$(PIP) install -r $(REQUIREMENTS_TXT)

install_kivy_requirements:
	@sudo apt install python3-pygame python3-opengl python3-enchant python3-opencv libgl1-mesa-dev libgles2-mesa-dev zlib1g-dev libzbar-dev xclip wkhtmltopdf

install: install_kivy_requirements venv

update:
	@git fetch
	@git reset --hard origin/master

run:
	@$(PYTHON) main.py

