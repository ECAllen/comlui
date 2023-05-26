install:
	pip3 install --upgrade pip &&\
		pip3 install -r requirements.txt

snapshot:
	pip3 freeze > requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C *.py

test:
	# TODO: Add tests here
