compose-up:
	docker-compose up -d

compose-start:
	docker-compose start

compose-stop:
	docker-compose stop

compose-down:
	docker-compose down -v

unit-tests:
	python -m unittest tests/unit.py

integration-tests:
	python -m unittest tests/integration.py