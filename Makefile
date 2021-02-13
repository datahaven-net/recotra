# This Makefile requires the following commands to be available:
# * virtualenv
# * python3.6

REQUIREMENTS_TXT:=requirements.txt

PIP:="venv/bin/pip"
PYTHON="venv/bin/python"
PYTHON_VERSION=python3.7

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
	@$(PIP) install Cython pygments docutils pillow
	@$(PIP) install -r $(REQUIREMENTS_TXT)

install_python37:
	@sudo apt update
	@sudo apt install software-properties-common
	@sudo add-apt-repository ppa:deadsnakes/ppa
	@sudo apt install python3.7
	@sudo apt install python3.7-venv
	@sudo apt install python3.7-dev

install_kivy_requirements:
	@sudo apt install python3-pygame python3-opengl python3-enchant python3-opencv libgl1-mesa-dev libgles2-mesa-dev zlib1g-dev libzbar-dev xclip wkhtmltopdf

install: install_python37 install_kivy_requirements venv

update:
	@git fetch
	@git reset --hard origin/master

run:
	@$(PYTHON) main.py
