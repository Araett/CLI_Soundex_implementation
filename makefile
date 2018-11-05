default:
	$(error Please use "make install")
install:
	pipenv install
	pipenv install -e .

